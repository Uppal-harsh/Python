"""
🚀 SENTINEL ANPR SYSTEM - RPi 4B OPTIMIZED
==========================================
PHASE 1: Install Dependencies
   $ sudo apt update && sudo apt install -y python3-opencv libcamera-dev rpicam-apps
   $ pip3 install ultralytics easyocr pyserial fpdf2

PHASE 2: Model Preparation
   1. Place your YOLOv8 model in: ./models/best.pt
   2. (Recommended) Export to NCNN for speed: model.export(format="ncnn")

PHASE 3: Hardware Setup
   - Connect RPi Camera (v2, v3, or HQ)
   - Connect SIM800L to GPIO Pins 14/15 (TX/RX)
   - Ensure Serial Port is enabled in raspi-config

PHASE 4: Run System
   $ cd ~/anpr_project && python3 main.py
==========================================
"""
import cv2
import time
import os
import datetime
from ultralytics import YOLO
from camera import CameraManager
from ocr import OCRManager
from gsm import GSMManager
from challan import ChallanGenerator
import config

def main():
    print("🚀 Starting Integrated ANPR System...")
    
    # Initialize components
    try:
        model = YOLO(config.MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}. Ensure {config.MODEL_PATH} exists.")
        return

    cam = CameraManager()
    ocr = OCRManager()
    gsm = GSMManager()
    challan = ChallanGenerator()

    # Trackers for violation logic
    # Dictionary format: {plate_text: {"first_seen": timestamp, "last_image": path}}
    tracking_vehicles = {}

    # Performance track
    frame_count = 0

    try:
        while True:
            original_frame, processed_frame = cam.get_frame()
            if original_frame is None:
                break

            frame_count += 1
            # 1. Performance Optimization: Only run YOLO every Nth frame
            if frame_count % config.DETECTION_INTERVAL != 0:
                cv2.imshow("ANPR Live (Monitoring)", original_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
                continue

            # 2. Plate Detection (Suggest using .ncnn format on RPi 4)
            # If you exported via model.export(format="ncnn"), use that path!
            results = model(original_frame, conf=config.CONFIDENCE_THRESHOLD, verbose=False, imgsz=640)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # 2. Crop and OCR
                    plate_crop = original_frame[y1:y2, x1:x2]
                    if plate_crop.size == 0: continue
                    
                    plate_text, enhanced_plate = ocr.read_plate(plate_crop)
                    
                    if plate_text:
                        print(f"🔍 Detected Plate: {plate_text}")
                        
                        # 3. Violation Logic (Timer based)
                        now = time.time()
                        if plate_text not in tracking_vehicles:
                            # Save initial capture
                            cap_path = os.path.join(config.CAPTURES_DIR, f"{plate_text}_init.jpg")
                            cv2.imwrite(cap_path, original_frame)
                            tracking_vehicles[plate_text] = {
                                "first_seen": now,
                                "last_seen": now,
                                "image_path": cap_path
                            }
                        else:
                            # Check if duration exceeds threshold for "No Parking" violation
                            duration = now - tracking_vehicles[plate_text]["first_seen"]
                            tracking_vehicles[plate_text]["last_seen"] = now
                            
                            if duration > config.VIOLATION_TIMER_SECONDS:
                                print(f"🚨 VIOLATION: {plate_text} stayed for {int(duration)}s")
                                
                                # Generate Challan
                                challan_path = challan.generate(plate_text, "No Parking Violation", tracking_vehicles[plate_text]["image_path"])
                                
                                # Send Notification
                                gsm.send_sms(config.ADMIN_PHONE, f"Violation Alert!\nPlate: {plate_text}\nType: No Parking\nTime: {datetime.datetime.now()}")
                                
                                # Remove from active tracking to prevent multiple triggers
                                del tracking_vehicles[plate_text]

            # Cleanup tracking (remove vehicles not seen for 10 seconds)
            current_time = time.time()
            to_delete = [p for p, data in tracking_vehicles.items() if current_time - data["last_seen"] > 10]
            for p in to_delete: del tracking_vehicles[p]

            # Display (Optional - remove for headless RPi performance)
            cv2.imshow("ANPR Live Feed", original_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cam.release()
        gsm.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
