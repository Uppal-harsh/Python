"""
YOLO + EasyOCR License Plate Detection Pipeline
Uses YOLOv8 for vehicle detection and EasyOCR for plate text recognition.
"""

import re
import io
import base64
import numpy as np
from PIL import Image

# ── Lazy-loaded models (loaded on first use to speed up server start) ──
_yolo_model = None
_ocr_reader = None

# COCO class IDs for vehicles
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

# Indian plate pattern regex — matches formats like DL 3C AB 1234, MH12AB3456, etc.
PLATE_PATTERN = re.compile(
    r'[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,3}\s*\d{4}',
    re.IGNORECASE
)


def get_yolo_model():
    """Lazy-load YOLOv8 nano model (downloads ~6MB on first run)."""
    global _yolo_model
    if _yolo_model is None:
        from ultralytics import YOLO
        _yolo_model = YOLO("yolov8n.pt")
        print("[YOLO] Model loaded successfully")
    return _yolo_model


def get_ocr_reader():
    """Lazy-load EasyOCR reader (downloads models on first run)."""
    global _ocr_reader
    if _ocr_reader is None:
        import easyocr
        _ocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        print("[EasyOCR] Reader initialized")
    return _ocr_reader


def decode_base64_image(base64_str):
    """Decode a base64-encoded image string to a numpy array (RGB)."""
    # Strip data URL prefix if present (e.g. "data:image/png;base64,...")
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]

    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    return np.array(image)


def format_plate(raw_text):
    """
    Format a raw matched plate string into standard Indian format.
    Input:  'DL3CAB1234' or 'DL 3C AB 1234'
    Output: 'DL 03 AB 1234'
    """
    text = re.sub(r"\s+", "", raw_text).upper()

    match = re.match(r"([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{4})", text)
    if match:
        state = match.group(1)
        district = match.group(2).zfill(2)
        series = match.group(3)
        number = match.group(4)
        return f"{state} {district} {series} {number}"

    return raw_text.upper()


def _ocr_on_region(reader, img_array):
    """Run EasyOCR on an image region and extract plate-like strings."""
    plates = []
    try:
        ocr_results = reader.readtext(img_array)
        for (_bbox, text, conf) in ocr_results:
            cleaned = text.strip().upper()
            match = PLATE_PATTERN.search(cleaned)
            if match:
                plate_text = format_plate(match.group())
                plates.append({
                    "plate": plate_text,
                    "confidence": round(conf, 2),
                    "raw_text": cleaned,
                })
    except Exception as e:
        print(f"[OCR Error] {e}")
    return plates


def detect_plate(base64_image):
    """
    Full detection pipeline:
      1. Decode base64 image
      2. YOLOv8 detects vehicles in the frame
      3. EasyOCR reads text from vehicle bounding-box crops
      4. Regex filters for Indian plate patterns
      5. Falls back to full-image OCR if no plates found in crops

    Returns dict with vehicles, plates, and best_plate.
    """
    # Decode image
    img = decode_base64_image(base64_image)
    h, w = img.shape[:2]

    # ── YOLO vehicle detection ──
    model = get_yolo_model()
    results = model(img, conf=0.25, verbose=False)

    vehicles_found = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if cls_id in VEHICLE_CLASSES:
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                vehicles_found.append({
                    "class_name": VEHICLE_CLASSES[cls_id],
                    "confidence": round(conf, 2),
                    "bbox": [x1, y1, x2, y2],
                })

    # ── OCR plate reading ──
    reader = get_ocr_reader()
    detected_plates = []

    # Strategy 1: OCR on each detected vehicle crop
    if vehicles_found:
        for v in vehicles_found:
            x1, y1, x2, y2 = v["bbox"]
            # Add 10% padding around the bounding box for better plate capture
            pad_x = int((x2 - x1) * 0.1)
            pad_y = int((y2 - y1) * 0.1)
            crop = img[
                max(0, y1 - pad_y): min(h, y2 + pad_y),
                max(0, x1 - pad_x): min(w, x2 + pad_x),
            ]
            if crop.size > 0:
                plates = _ocr_on_region(reader, crop)
                for p in plates:
                    p["source"] = "vehicle_crop"
                detected_plates.extend(plates)

    # Strategy 2: Fallback — OCR on the full image
    if not detected_plates:
        plates = _ocr_on_region(reader, img)
        for p in plates:
            p["source"] = "full_image"
        detected_plates.extend(plates)

    # Deduplicate plates (same plate string)
    seen = set()
    unique_plates = []
    for p in detected_plates:
        if p["plate"] not in seen:
            seen.add(p["plate"])
            unique_plates.append(p)

    # Sort by confidence (highest first)
    unique_plates.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "vehicles_detected": len(vehicles_found),
        "vehicles": vehicles_found,
        "plates": unique_plates,
        "best_plate": unique_plates[0]["plate"] if unique_plates else None,
    }


def is_available():
    """Check if YOLO and EasyOCR dependencies are importable."""
    try:
        import ultralytics  # noqa: F401
        import easyocr  # noqa: F401
        return True
    except ImportError:
        return False
