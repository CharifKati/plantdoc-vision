"""
sanitizer.py
------------
Strips sensitive internals from the model response before it reaches
the client. Prevents accidental leakage of file paths, model internals,
layer names, or stack traces.
"""

# Keys allowed to leave the server — covers PredictResponse + PredictionItem fields
ALLOWED_KEYS = {
    # Top-level response
    "id",
    "timestamp",
    "predictions",
    "low_confidence",
    "image_b64",
    "heatmap_b64",
    "error",
    "detail",
    # Per-prediction item
    "class_name",
    "display_name",
    "confidence",
    "confidence_pct",
    "status",
    "severity",
    "description",
    "actions",
    "color",
    # Low-confidence / unknown path
    "uncertain",
    "message",
    "consult_expert",
    "symptoms",
}

# Keys that should NEVER leave the server (examples of what we're blocking)
# - file paths, model layer names, stack traces, internal debug info
# Anything not in ALLOWED_KEYS above is implicitly blocked.


def sanitize_response(raw: dict) -> dict:
    """
    Recursively removes any key not in ALLOWED_KEYS.

    Usage:
        return sanitize_response(response.dict())
    """
    return _clean(raw)


def _clean(obj):
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items() if k in ALLOWED_KEYS}
    if isinstance(obj, list):
        return [_clean(i) for i in obj]
    return obj