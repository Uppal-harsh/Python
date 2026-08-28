import os

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models/best.pt") 
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CHALLANS_DIR = os.path.join(BASE_DIR, "challans")
CAPTURES_DIR = os.path.join(BASE_DIR, "captures")

# Camera Settings (Optimized for RPi 4 HQ/V3 Camera)
CAMERA_WIDTH = 1296
CAMERA_HEIGHT = 972
CAMERA_FPS = 30
SHARPNESS = 2.0
CONTRAST = 1.2
BRIGHTNESS = 0.1

# Detection & OCR Settings
CONFIDENCE_THRESHOLD = 0.5
PLATE_RESIZE_DIM = (333, 75)
VIOLATION_TIMER_SECONDS = 5 

# Performance Tweaks for RPi 4
DETECTION_INTERVAL = 2  
USE_NCNN = True         

# GSM/SIM800L Settings
# RPi 4 Serial Ports: /dev/ttyS0 (Mini) or /dev/ttyAMA0 (Hardware)
SERIAL_PORT = "/dev/ttyS0" 
BAUD_RATE = 9600
ADMIN_PHONE = "+91XXXXXXXXXX"

# Database Settings
DB_NAME = os.path.join(BASE_DIR, "anpr_system.db")
USE_GPS = False
