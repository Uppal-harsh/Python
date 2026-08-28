"""
Smart No-Parking Zone Violation Detection System — Flask Backend
Main application entry point with all REST API endpoints.
Serves the frontend dashboard at the root URL.
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime

import database as db
from plate_generator import generate_plate
from enforcement import start_enforcement_thread, get_random_location, get_random_gps

import sys
sys.path.append(r'c:\pylibs')

# Try to import the YOLO+OCR plate detector (optional heavy dependency)
try:
    import plate_detector
    PLATE_DETECTOR_AVAILABLE = plate_detector.is_available()
except ImportError:
    PLATE_DETECTOR_AVAILABLE = False

# Resolve the frontend directory path
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)  # Enable CORS for all routes


# ──────────────────────────────────────────────
#   API ENDPOINTS
# ──────────────────────────────────────────────

@app.route("/api/vehicle/detect", methods=["POST"])
def detect_vehicle():
    """
    Register a new vehicle entering the no-parking zone.
    Optionally accepts JSON body with 'plate'. If not provided,
    auto-generates a random Indian number plate.
    """
    data = request.get_json(silent=True) or {}
    plate = data.get("plate") or generate_plate()

    # Prevent duplicate active entries
    if plate in db.vehicles:
        return jsonify({"error": "Vehicle already being tracked", "plate": plate}), 409

    location = get_random_location()
    gps = get_random_gps()
    vehicle = db.add_vehicle(plate, location, gps)

    return jsonify({
        "message": "Vehicle detected and tracking started",
        "plate": vehicle["plate"],
        "entry_time": vehicle["entry_time"],
        "location": vehicle["location"],
        "gps": vehicle["gps"],
        "status": vehicle["status"],
    }), 201


@app.route("/api/vehicles", methods=["GET"])
def get_vehicles():
    """Return all currently tracked vehicles with elapsed time."""
    vehicles = db.get_all_vehicles()
    return jsonify({"vehicles": vehicles, "count": len(vehicles)})


@app.route("/api/vehicle/exit", methods=["POST"])
def vehicle_exit():
    """
    Mark a vehicle as having left the zone.
    Expects JSON body with 'plate'.
    """
    data = request.get_json(silent=True) or {}
    plate = data.get("plate")

    if not plate:
        return jsonify({"error": "Number plate is required"}), 400

    vehicle = db.remove_vehicle(plate)
    if vehicle:
        return jsonify({
            "message": "Vehicle removed from tracking",
            "plate": plate,
            "was_status": vehicle["status"],
        })
    else:
        return jsonify({"error": "Vehicle not found in active tracking"}), 404


@app.route("/api/sms-log", methods=["GET"])
def get_sms_log():
    """Return all simulated SMS messages sent."""
    log = db.get_sms_log()
    return jsonify({"sms_log": log, "count": len(log)})


@app.route("/api/challans", methods=["GET"])
def get_challans():
    """Return all issued challans."""
    challans = db.get_challans()
    return jsonify({"challans": challans, "count": len(challans)})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return dashboard statistics."""
    stats = db.get_stats()
    return jsonify(stats)


@app.route("/api/scan-plate", methods=["POST"])
def scan_plate():
    """
    Accept a base64-encoded webcam frame, run YOLO vehicle detection
    and EasyOCR plate recognition, then auto-register the detected plate.
    """
    if not PLATE_DETECTOR_AVAILABLE:
        return jsonify({
            "error": "YOLO/EasyOCR not installed. Run: pip install ultralytics easyocr opencv-python-headless",
            "available": False,
        }), 503

    data = request.get_json(silent=True) or {}
    image_b64 = data.get("image")

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Run the YOLO + EasyOCR pipeline
        result = plate_detector.detect_plate(image_b64)

        # If a plate was detected, auto-register it in the database
        auto_registered = False
        if result["best_plate"]:
            plate = result["best_plate"]
            if plate not in db.vehicles:
                location = get_random_location()
                gps = get_random_gps()
                db.add_vehicle(plate, location, gps)
                auto_registered = True

        return jsonify({
            "vehicles_detected": result["vehicles_detected"],
            "vehicles": result["vehicles"],
            "plates": result["plates"],
            "best_plate": result["best_plate"],
            "auto_registered": auto_registered,
        })

    except Exception as e:
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500


@app.route("/api/detector-status", methods=["GET"])
def detector_status():
    """Check if YOLO and EasyOCR are available."""
    return jsonify({"available": PLATE_DETECTOR_AVAILABLE})


@app.route("/", methods=["GET"])
def index():
    """Serve the frontend dashboard."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "system": "Smart No-Parking Zone Violation Detection System",
        "status": "Online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "yolo_available": PLATE_DETECTOR_AVAILABLE,
    })


# ──────────────────────────────────────────────
#   START SERVER
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  🚗 Smart No-Parking Zone Violation Detection System")
    print("  🔧 Backend Server Starting...")
    print("=" * 60)

    # Start the background enforcement thread
    start_enforcement_thread(check_interval=10)

    print(f"\n  ✅ Server running at http://localhost:5000")
    print(f"  📡 API endpoints ready")
    print(f"  🔍 Enforcement thread active (checking every 10s)")
    if PLATE_DETECTOR_AVAILABLE:
        print(f"  🤖 YOLO + EasyOCR plate detection: ENABLED")
    else:
        print(f"  ⚠️  YOLO + EasyOCR plate detection: DISABLED")
        print(f"      Install with: pip install ultralytics easyocr opencv-python-headless")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=False)
