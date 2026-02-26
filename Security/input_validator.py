"""
input_validator.py
------------------
First line of defense. Runs before anything touches the model.
Blocks bad file types, oversized files, unreadable images,
invalid dimensions, and severely blurry photos.
"""

import cv2
import numpy as np

MAX_FILE_SIZE  = 10 * 1024 * 1024   # 10 MB
ALLOWED_TYPES  = {"image/jpeg", "image/png", "image/webp"}
BLUR_THRESHOLD = 2.0                 # Laplacian variance — only blocks pure solid-colour or blank images
MIN_DIM        = 64                  # pixels
MAX_DIM        = 4096                # pixels


def validate_file_type(content_type: str) -> tuple[bool, str]:
    if content_type not in ALLOWED_TYPES:
        return False, f"Invalid file type '{content_type}' — accepted: jpeg, png, webp"
    return True, ""


def validate_file_size(data: bytes) -> tuple[bool, str]:
    if len(data) > MAX_FILE_SIZE:
        mb = len(data) / (1024 * 1024)
        return False, f"File too large ({mb:.1f} MB) — maximum is 10 MB"
    return True, ""


def validate_image_readable(data: bytes) -> tuple[bool, str, any]:
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return False, "File could not be decoded as an image", None
    return True, "", img


def validate_dimensions(img: np.ndarray) -> tuple[bool, str]:
    h, w = img.shape[:2]
    if h < MIN_DIM or w < MIN_DIM:
        return False, f"Image too small ({w}x{h}px) — minimum is {MIN_DIM}x{MIN_DIM}px"
    if h > MAX_DIM or w > MAX_DIM:
        return False, f"Image too large ({w}x{h}px) — maximum is {MAX_DIM}x{MAX_DIM}px"
    return True, ""


def validate_blur(img: np.ndarray) -> tuple[bool, str]:
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    if score < BLUR_THRESHOLD:
        return False, f"Image appears to be a solid colour or completely blank (score {score:.1f}) — please upload a real photo"
    return True, ""


def run_all_checks(content_type: str, data: bytes) -> tuple[bool, str, any]:
    """
    Master validation call — use this from main.py.
    Returns (is_valid, error_message, img_array | None)

    Usage:
        ok, error, img = run_all_checks(file.content_type, await file.read())
        if not ok:
            return {"error": error}
    """
    # Checks before decoding
    for fn, args in [
        (validate_file_type, (content_type,)),
        (validate_file_size, (data,)),
    ]:
        ok, msg = fn(*args)
        if not ok:
            return False, msg, None

    # Decode
    ok, msg, img = validate_image_readable(data)
    if not ok:
        return False, msg, None

    # Checks after decoding
    for fn in [validate_dimensions, validate_blur]:
        ok, msg = fn(img)
        if not ok:
            return False, msg, None

    return True, "", img