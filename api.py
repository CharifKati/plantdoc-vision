"""
PlantDoc Vision - FastAPI Backend v4 (Unified PyTorch)
Merges:
  - PyTorch MobileNetV2 model inference
  - Security layer (rate limiting, IP banning, input validation)
  - Grad-CAM heatmaps (pure PyTorch — no TensorFlow dependency)
  - Geo-tagging & disease map endpoint

Run:
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
"""

import os
import io
import json
import uuid
import base64
from datetime import datetime
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image
from slowapi.errors import RateLimitExceeded

# ── Security layer ──
from Security import (
    run_all_checks,
    sanitize_response,
    is_banned,
    record_strike,
    limiter,
    PREDICT_LIMIT,
    rate_limit_exceeded_handler,
    log_blocked,
    log_allowed,
    get_stats,
    get_log_feed,
)

# ── Advice library ──
from plant_advice import get_advice


# ─────────────────────────── Config ───────────────────────────────────────────

MODEL_SAVE_PATH      = os.environ.get("MODEL_PATH",       "plantdoc_model_base.pth")
CLASS_NAMES_PATH     = os.environ.get("CLASS_NAMES_PATH", "class_names.json")
IMG_SIZE             = (224, 224)
CONFIDENCE_THRESHOLD = 0.35
DEVICE               = torch.device("cuda" if torch.cuda.is_available() else "cpu")

torch_model:          Optional[nn.Module] = None
class_names_global:   List[str]           = []
history_store:        List[dict]          = []


# ─────────────────────────── App setup ────────────────────────────────────────

app = FastAPI(title="PlantDoc Vision API", version="4.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────── Model loading ────────────────────────────────────

def load_pytorch_model(num_classes: int) -> nn.Module:
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(model.last_channel, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes),
    )
    model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model


@app.on_event("startup")
async def startup_event():
    global torch_model, class_names_global

    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH) as f:
            class_names_global = json.load(f)
        print(f"{len(class_names_global)} classes loaded.")
    else:
        print("class_names.json not found.")
        return

    if os.path.exists(MODEL_SAVE_PATH):
        torch_model = load_pytorch_model(len(class_names_global))
        print(f"PyTorch model loaded from {MODEL_SAVE_PATH} on {DEVICE}")
    else:
        print(f"Model not found at {MODEL_SAVE_PATH}")


# ─────────────────────────── Image transforms ─────────────────────────────────

infer_transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])


def preprocess_image(image_bytes: bytes) -> torch.Tensor:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return infer_transform(img).unsqueeze(0).to(DEVICE)


# ─────────────────────────── Grad-CAM (PyTorch) ───────────────────────────────

def generate_gradcam(
    model:       nn.Module,
    tensor:      torch.Tensor,
    class_idx:   int,
    image_bytes: bytes,
) -> Optional[str]:
    """
    Compute a Grad-CAM heatmap and composite it over the original leaf image.

    Returns a base64-encoded PNG where the JET heatmap is alpha-blended on top
    of the resized leaf photo, so diseased regions are clearly highlighted while
    the leaf itself remains fully visible underneath.
    """
    try:
        gradients:  List[torch.Tensor] = []
        activations: List[torch.Tensor] = []

        def save_gradient(grad):
            gradients.append(grad)

        def forward_hook(module, inp, out):
            activations.append(out)
            out.register_hook(save_gradient)

        # Hook the last feature block of MobileNetV2
        target_layer = model.features[-1]
        hook = target_layer.register_forward_hook(forward_hook)

        # Forward + backward
        model.zero_grad()
        output = model(tensor)
        score  = output[0, class_idx]
        score.backward()

        hook.remove()

        if not gradients or not activations:
            return None

        grads = gradients[0]   # (1, C, H, W)
        acts  = activations[0] # (1, C, H, W)

        # Global-average-pool gradients → per-channel weights
        weights = grads.mean(dim=(2, 3), keepdim=True)  # (1, C, 1, 1)

        # Weighted sum of activation maps + ReLU
        cam = (weights * acts).sum(dim=1, keepdim=True)  # (1, 1, H, W)
        cam = F.relu(cam)

        # Normalise to [0, 1]
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max - cam_min < 1e-8:
            return None
        cam = (cam - cam_min) / (cam_max - cam_min)

        # Upsample CAM to full image size
        cam_up = F.interpolate(cam, size=IMG_SIZE, mode="bilinear", align_corners=False)
        cam_np = (cam_up.squeeze().detach().cpu().numpy() * 255).astype(np.uint8)

        # ── Build the composite: leaf + heatmap overlay ──

        # 1. Resize original leaf to the standard size (RGB base layer)
        leaf_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(
            IMG_SIZE, Image.BILINEAR
        )

        # 2. Produce a semi-transparent JET heatmap (RGBA)
        heatmap_rgba = _apply_jet_colormap(cam_np)

        # 3. Alpha-composite: heatmap over leaf
        #    PIL.Image.alpha_composite needs both images in RGBA mode
        leaf_rgba   = leaf_img.convert("RGBA")
        composite   = Image.alpha_composite(leaf_rgba, heatmap_rgba)

        # 4. Back to RGB for a clean PNG output
        result = composite.convert("RGB")

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()

    except Exception as e:
        print(f"⚠ Grad-CAM failed: {e}")
        return None


def _apply_jet_colormap(gray: np.ndarray, alpha: int = 165) -> Image.Image:
    """
    Convert a 2-D uint8 grayscale array to a JET-coloured RGBA PIL image.

    `alpha` controls heatmap opacity (0 = invisible, 255 = fully opaque).
    165 ≈ 65 % opacity — bright enough to show hotspots, low enough to see the leaf.

    Cool areas (low activation) are made more transparent so the leaf is
    clearly visible where nothing interesting is happening.
    """
    t = gray / 255.0  # [0, 1]

    # JET colour ramp
    r = np.clip(1.5 - np.abs(t * 4 - 3), 0, 1)
    g = np.clip(1.5 - np.abs(t * 4 - 2), 0, 1)
    b = np.clip(1.5 - np.abs(t * 4 - 1), 0, 1)

    # Scale alpha by activation strength: cold spots become nearly transparent
    a = (t * alpha).astype(np.uint8)

    rgba = np.stack(
        [(r * 255).astype(np.uint8),
         (g * 255).astype(np.uint8),
         (b * 255).astype(np.uint8),
         a],
        axis=-1,
    )
    return Image.fromarray(rgba, mode="RGBA")


# ─────────────────────────── Pydantic models ──────────────────────────────────

class PredictionItem(BaseModel):
    class_name:     str
    display_name:   str
    confidence:     float
    confidence_pct: str
    status:         str
    severity:       str
    description:    str
    actions:        List[str]
    color:          str


class PredictResponse(BaseModel):
    id:             str
    timestamp:      str
    predictions:    List[PredictionItem]
    low_confidence: bool
    image_b64:      Optional[str] = None
    heatmap_b64:    Optional[str] = None


# ─────────────────────────── Helpers ──────────────────────────────────────────

SEVERITY_COLORS = {
    "none":     "#22c55e",
    "low":      "#eab308",
    "medium":   "#f97316",
    "high":     "#ef4444",
    "critical": "#dc2626",
    "unknown":  "#6b7280",
}


def format_display_name(raw: str) -> str:
    parts = raw.replace("__", "|||").replace("_", " ").split("|||")
    if len(parts) == 2:
        return parts[0].strip().title() + " - " + parts[1].strip().title()
    return raw.replace("_", " ").title()


def _build_prediction_item(class_name: str, confidence: float) -> PredictionItem:
    adv          = get_advice(class_name)
    status_raw   = adv.get("status",   "unknown")
    severity_raw = adv.get("severity", "unknown")
    color        = SEVERITY_COLORS.get(severity_raw, "#6b7280")
    display_name = adv.get("display_name") or format_display_name(class_name)

    return PredictionItem(
        class_name     = class_name,
        display_name   = display_name,
        confidence     = round(confidence, 4),
        confidence_pct = str(round(confidence * 100, 1)) + "%",
        status         = status_raw.capitalize(),
        severity       = severity_raw,
        description    = adv.get("description", ""),
        actions        = adv.get("actions", []),
        color          = color,
    )


# ─────────────────────────── Endpoints ───────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status":       "ok",
        "model_loaded": torch_model is not None,
        "num_classes":  len(class_names_global),
        "device":       str(DEVICE),
    }


@app.get("/classes")
def get_classes():
    return {"classes": class_names_global, "count": len(class_names_global)}


@app.post("/predict", response_model=PredictResponse)
@limiter.limit(PREDICT_LIMIT)
async def predict_endpoint(
    request: Request,
    file:    UploadFile        = File(...),
    lat:     Optional[float]   = Form(None),
    lng:     Optional[float]   = Form(None),
):
    ip = request.client.host

    if is_banned(ip):
        raise HTTPException(403, "Access denied.")

    if torch_model is None:
        raise HTTPException(503, "Model not loaded. Run Train.py first.")
    if not class_names_global:
        raise HTTPException(503, "class_names.json missing.")

    contents = await file.read()
    ok, error, _img_cv2 = run_all_checks(file.content_type, contents)
    if not ok:
        log_blocked(ip, error)
        record_strike(ip)
        raise HTTPException(400, error)

    try:
        tensor = preprocess_image(contents)

        with torch.no_grad():
            output = torch_model(tensor)
            probs  = torch.softmax(output, dim=1)[0].cpu().numpy()

        top3_idx = np.argsort(probs)[-3:][::-1]
        results  = [
            _build_prediction_item(class_names_global[idx], float(probs[idx]))
            for idx in top3_idx
        ]

        low_confidence = float(probs[top3_idx[0]]) < CONFIDENCE_THRESHOLD
        img_b64        = base64.b64encode(contents).decode()
        entry_id       = str(uuid.uuid4())[:8]
        timestamp      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ── Grad-CAM (requires grad, so run outside torch.no_grad) ──
        heatmap_b64 = None
        try:
            # Re-run with a fresh tensor so gradients flow
            tensor_grad = preprocess_image(contents).requires_grad_(True)
            heatmap_b64 = generate_gradcam(torch_model, tensor_grad, int(top3_idx[0]), contents)
        except Exception as e:
            print(f"⚠ Grad-CAM skipped: {e}")

        history_store.insert(0, {
            "id":             entry_id,
            "timestamp":      timestamp,
            "filename":       file.filename,
            "top_prediction": results[0].display_name,
            "top_confidence": results[0].confidence_pct,
            "severity":       results[0].severity,
            "color":          results[0].color,
            "image_b64":      img_b64,
            "predictions":    [r.dict() for r in results],
            "low_confidence": low_confidence,
            "heatmap_b64":    heatmap_b64,
            "lat":            lat,
            "lng":            lng,
        })
        if len(history_store) > 50:
            history_store.pop()

        log_allowed(ip)
        return sanitize_response(PredictResponse(
            id             = entry_id,
            timestamp      = timestamp,
            predictions    = results,
            low_confidence = low_confidence,
            image_b64      = img_b64,
            heatmap_b64    = heatmap_b64,
        ).dict())

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, "Prediction failed: " + str(e))


@app.get("/history")
def get_history():
    return {"history": history_store, "count": len(history_store)}


@app.delete("/history")
def clear_history():
    history_store.clear()
    return {"message": "History cleared"}


@app.get("/map")
def get_map_data():
    """Return geo-tagged scan entries for the disease distribution map."""
    geo_entries = [
        {
            "id":             e["id"],
            "lat":            e["lat"],
            "lng":            e["lng"],
            "top_prediction": e["top_prediction"],
            "severity":       e["severity"],
            "color":          e["color"],
            "timestamp":      e["timestamp"],
        }
        for e in history_store
        if e.get("lat") is not None and e.get("lng") is not None
    ]
    return {"points": geo_entries, "count": len(geo_entries)}


@app.get("/demo")
def list_demo():
    demo_dir = "demo_images"
    if not os.path.exists(demo_dir):
        return {"images": []}
    images = [
        f for f in os.listdir(demo_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    return {"images": images}


@app.get("/demo/{filename}")
def get_demo(filename: str):
    path = os.path.join("demo_images", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Demo image not found.")
    return FileResponse(path)


@app.get("/security/stats")
def security_stats():
    return {"stats": get_stats(), "log": get_log_feed()}


@app.get("/security")
def security_dashboard():
    path = os.path.join("frontend", "security.html")
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(404, "Security dashboard not found.")


if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")