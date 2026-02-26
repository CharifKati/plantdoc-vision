"""
PlantDoc Vision — Disease Advice Library + Inference Utilities
"""

import json
import torch
import torch.nn.functional as F
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import io

IMG_SIZE = 224

# ── Advice library ────────────────────────────────────────────────────────────
# Keys are partial matches against class names (lowercase)
ADVICE_DB = {
    "healthy": {
        "status": "healthy",
        "severity": "none",
        "title": "Plant looks healthy!",
        "actions": [
            "Continue regular watering and fertilization schedule.",
            "Monitor weekly for early signs of stress or discoloration.",
            "Ensure adequate sunlight and air circulation.",
        ],
        "note": "No action required. Keep up good practices.",
    },
    "late_blight": {
        "status": "disease",
        "severity": "high",
        "title": "Late Blight Detected",
        "actions": [
            "Remove and destroy all infected leaves immediately — do not compost.",
            "Apply copper-based fungicide or chlorothalonil spray.",
            "Avoid overhead watering; water at the base in the morning.",
            "Isolate affected plants to prevent spread.",
        ],
        "note": "Late blight spreads rapidly in cool, wet conditions. Act quickly.",
    },
    "early_blight": {
        "status": "disease",
        "severity": "medium",
        "title": "Early Blight Detected",
        "actions": [
            "Remove lower infected leaves and dispose of them away from the garden.",
            "Apply fungicide containing chlorothalonil or mancozeb every 7–10 days.",
            "Mulch around the base to reduce soil splash.",
            "Improve spacing between plants for better airflow.",
        ],
        "note": "Early blight is manageable if caught early.",
    },
    "bacterial_spot": {
        "status": "disease",
        "severity": "medium",
        "title": "Bacterial Spot Detected",
        "actions": [
            "Remove and destroy heavily infected leaves.",
            "Apply copper-based bactericide spray.",
            "Avoid working with plants when they are wet.",
            "Use drip irrigation instead of overhead sprinklers.",
        ],
        "note": "Bacterial spot spreads through water splash and tools.",
    },
    "leaf_mold": {
        "status": "disease",
        "severity": "medium",
        "title": "Leaf Mold Detected",
        "actions": [
            "Improve greenhouse ventilation and reduce humidity below 85%.",
            "Remove and destroy infected leaves.",
            "Apply fungicides containing chlorothalonil or mancozeb.",
            "Space plants further apart for air circulation.",
        ],
        "note": "Leaf mold thrives in humid, warm greenhouse conditions.",
    },
    "septoria": {
        "status": "disease",
        "severity": "medium",
        "title": "Septoria Leaf Spot Detected",
        "actions": [
            "Remove infected lower leaves promptly.",
            "Apply fungicide (chlorothalonil, copper, or mancozeb) every 10–14 days.",
            "Avoid wetting foliage when watering.",
            "Rotate crops next season.",
        ],
        "note": "Spreads upward from the ground; catch early to limit damage.",
    },
    "spider_mite": {
        "status": "pest",
        "severity": "medium",
        "title": "Spider Mite Infestation Detected",
        "actions": [
            "Spray undersides of leaves with strong water jets to dislodge mites.",
            "Apply insecticidal soap or neem oil every 5–7 days.",
            "Increase humidity around plants (mites prefer dry conditions).",
            "Introduce predatory mites (Phytoseiidae) as biological control.",
        ],
        "note": "Spider mites reproduce fast — treat immediately.",
    },
    "target_spot": {
        "status": "disease",
        "severity": "medium",
        "title": "Target Spot Detected",
        "actions": [
            "Remove and destroy affected leaves.",
            "Apply fungicides with active ingredients like azoxystrobin or difenoconazole.",
            "Avoid excessive nitrogen fertilization.",
            "Ensure good air circulation.",
        ],
        "note": "Common in warm, humid climates. Monitor closely.",
    },
    "mosaic_virus": {
        "status": "disease",
        "severity": "high",
        "title": "Mosaic Virus Detected",
        "actions": [
            "Remove and destroy infected plants — no cure exists.",
            "Control aphid populations which spread the virus.",
            "Disinfect tools with 10% bleach solution.",
            "Plant virus-resistant varieties next season.",
        ],
        "note": "Viral diseases cannot be cured. Prevent spread by controlling vectors.",
    },
    "yellow_leaf_curl": {
        "status": "disease",
        "severity": "high",
        "title": "Yellow Leaf Curl Virus Detected",
        "actions": [
            "Remove and destroy infected plants immediately.",
            "Control whitefly populations with insecticidal soap or yellow sticky traps.",
            "Use reflective mulch to deter whiteflies.",
            "Plant resistant varieties in future.",
        ],
        "note": "Transmitted by whiteflies. Control the vector to prevent spread.",
    },
    "powdery_mildew": {
        "status": "disease",
        "severity": "medium",
        "title": "Powdery Mildew Detected",
        "actions": [
            "Apply potassium bicarbonate, neem oil, or sulfur-based fungicide.",
            "Remove and dispose of heavily infected leaves.",
            "Avoid overhead watering.",
            "Improve air circulation by pruning crowded growth.",
        ],
        "note": "Powdery mildew thrives in dry conditions with high humidity.",
    },
    "leaf_scorch": {
        "status": "disease",
        "severity": "low",
        "title": "Leaf Scorch Detected",
        "actions": [
            "Ensure consistent watering to avoid drought stress.",
            "Apply mulch to retain soil moisture.",
            "Protect plants from extreme heat and wind.",
            "Check soil pH and nutrient balance.",
        ],
        "note": "Often caused by environmental stress rather than a pathogen.",
    },
    "black_rot": {
        "status": "disease",
        "severity": "high",
        "title": "Black Rot Detected",
        "actions": [
            "Remove all infected plant material immediately.",
            "Apply copper-based fungicide.",
            "Improve drainage and avoid waterlogging.",
            "Rotate crops — do not plant susceptible crops in same spot for 2 years.",
        ],
        "note": "Black rot can devastate crops quickly in warm, wet weather.",
    },
    "esca": {
        "status": "disease",
        "severity": "high",
        "title": "Esca (Black Measles) Detected",
        "actions": [
            "Prune out infected wood during dry weather.",
            "Seal pruning wounds with fungicidal paste.",
            "Avoid water stress by maintaining regular irrigation.",
            "Consult an expert — Esca has no complete cure.",
        ],
        "note": "Esca is a complex grapevine disease. Consult a viticulture expert.",
    },
    "leaf_blight": {
        "status": "disease",
        "severity": "medium",
        "title": "Leaf Blight Detected",
        "actions": [
            "Remove and destroy infected leaves.",
            "Apply appropriate fungicide based on pathogen type.",
            "Avoid overhead irrigation.",
            "Increase plant spacing for better airflow.",
        ],
        "note": "Identify the specific blight type for targeted treatment.",
    },
    "haunglongbing": {
        "status": "disease",
        "severity": "high",
        "title": "Citrus Greening (HLB) Detected",
        "actions": [
            "Remove and destroy infected trees — no cure exists.",
            "Control Asian citrus psyllid with insecticides.",
            "Use certified disease-free planting material.",
            "Notify local agricultural authorities immediately.",
        ],
        "note": "HLB is one of the most destructive citrus diseases worldwide.",
    },
    "northern_leaf_blight": {
        "status": "disease",
        "severity": "medium",
        "title": "Northern Leaf Blight (Corn) Detected",
        "actions": [
            "Apply foliar fungicides containing azoxystrobin or propiconazole.",
            "Plant resistant hybrid varieties.",
            "Rotate crops with non-host plants.",
            "Plow under crop debris after harvest.",
        ],
        "note": "Yield losses can be significant if infection occurs before tasseling.",
    },
}

DEFAULT_ADVICE = {
    "status": "unknown",
    "severity": "unknown",
    "title": "Disease Detected",
    "actions": [
        "Isolate the affected plant from others.",
        "Observe the plant daily for changes.",
        "Consult a local agricultural expert or extension service.",
        "Take multiple photos from different angles for better diagnosis.",
    ],
    "note": "For accurate diagnosis, consult an agronomist.",
}


def get_advice(class_name: str) -> dict:
    """Match class name to advice entry."""
    name_lower = class_name.lower()
    for key, advice in ADVICE_DB.items():
        if key in name_lower:
            return advice
    return DEFAULT_ADVICE


# ── Model loading ─────────────────────────────────────────────────────────────
def load_model(model_path: str, device: torch.device):
    ckpt = torch.load(model_path, map_location=device)
    classes = ckpt["classes"]
    num_classes = ckpt["num_classes"]

    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_features, num_classes),
    )
    model.load_state_dict(ckpt["model_state"])
    model.to(device).eval()
    return model, classes


# ── Preprocessing ─────────────────────────────────────────────────────────────
preprocess = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

CONFIDENCE_THRESHOLD = 0.35


def predict(model, classes, image_bytes: bytes, device: torch.device, top_k: int = 3):
    """
    Returns list of top_k dicts:
      { class_name, confidence, advice }
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(tensor)
        probs  = F.softmax(logits, dim=1)[0]

    top_probs, top_idxs = probs.topk(top_k)
    results = []
    for prob, idx in zip(top_probs.tolist(), top_idxs.tolist()):
        class_name = classes[idx]
        results.append({
            "class_name":  class_name,
            "confidence":  round(prob, 4),
            "advice":      get_advice(class_name),
        })

    # Flag low-confidence prediction
    low_confidence = top_probs[0].item() < CONFIDENCE_THRESHOLD
    return results, low_confidence
