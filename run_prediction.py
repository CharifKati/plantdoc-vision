# this is the file to test the model on a single image and print the results in a human-friendly format

import sys
import numpy as np
from pathlib import Path

# ── Path fix ───────────────────────────────────────────────────────────────────
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))
# ──────────────────────────────────────────────────────────────────────────────

import tensorflow as tf
from inference import get_advice   # reuse the advice library from inference.py

# ── Config ─────────────────────────────────────────────────────────────────────
MODEL_PATH = str(_THIS_DIR / "plantdoc_model.h5")
IMG_SIZE   = (224, 224)
TOP_K      = 3

SEVERITY_COLORS = {
    "none":    "\033[92m",
    "low":     "\033[93m",
    "medium":  "\033[93m",
    "high":    "\033[91m",
    "unknown": "\033[0m",
}
RESET = "\033[0m"


def predict_keras(image_path: str, model, class_names: list, top_k: int = 3):
    img = tf.keras.utils.load_img(image_path, target_size=IMG_SIZE)
    arr = tf.keras.utils.img_to_array(img)
    arr = tf.expand_dims(arr, 0)                      # (1, 224, 224, 3)
    probs = model.predict(arr, verbose=0)[0]           # (num_classes,)

    top_idxs = np.argsort(probs)[-top_k:][::-1]
    return [
        {"class_name": class_names[i], "confidence": float(probs[i])}
        for i in top_idxs
    ]


def run(image_path: str):
    image_path = Path(image_path)

    if not image_path.exists():
        print(f"[ERROR] Image not found: {image_path}")
        sys.exit(1)

    if not Path(MODEL_PATH).exists():
        print(f"[ERROR] Model not found: {MODEL_PATH}")
        sys.exit(1)

    print(f"\n  Image : {image_path.name}")
    print(f"  Model : plantdoc_model.h5\n")
    print("=" * 52)
    print("  PlantDoc Vision — Diagnosis Results")
    print("=" * 52)

    # Load Keras model
    print("  Loading model...", end=" ", flush=True)
    model = tf.keras.models.load_model(MODEL_PATH)
    num_classes = model.output_shape[-1]
    print(f"OK  ({num_classes} classes)\n")

    # Recover class names from the training dataset directory
    # (same split used in Train.py)
    try:
        from Train import load_datasets
        _, _, class_names = load_datasets()
    except Exception:
        # Fallback: generate generic names if dataset isn't available
        class_names = [f"class_{i}" for i in range(num_classes)]
        print("  ⚠  Could not load class names from dataset — using generic labels.\n")

    # Run prediction
    results = predict_keras(str(image_path), model, class_names, top_k=TOP_K)

    for rank, result in enumerate(results, start=1):
        advice   = get_advice(result["class_name"])
        conf_pct = round(result["confidence"] * 100, 1)
        severity = advice.get("severity", "unknown")
        color    = SEVERITY_COLORS.get(severity, RESET)

        print(f"  #{rank}  {result['class_name']}")
        print(f"       Confidence : {conf_pct}%")
        print(f"       Status     : {color}{advice['status'].upper()}{RESET}")
        print(f"       Severity   : {color}{severity.upper()}{RESET}")
        print(f"       {advice['title']}")
        print()
        print("       Recommended Actions:")
        for action in advice["actions"]:
            print(f"         • {action}")
        print(f"\n       Note: {advice['note']}")
        print()
        if rank < len(results):
            print("  " + "-" * 48)

    print("=" * 52 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    run(sys.argv[1])