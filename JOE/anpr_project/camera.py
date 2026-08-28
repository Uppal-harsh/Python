import cv2
import numpy as np
import subprocess
from config import CAMERA_WIDTH, CAMERA_HEIGHT, SHARPNESS, CONTRAST, BRIGHTNESS

class CameraManager:
    def __init__(self):
        """
        Uses Picamera2 or rpicam-vid to get the exact hardware settings 
        required for optimized ANPR.
        """
        print("Initializing RPi Camera with ANPR optimizations...")
        self.cmd = [
            'rpicam-vid',
            '-t', '0',
            '--width', str(CAMERA_WIDTH),
            '--height', str(CAMERA_HEIGHT),
            '--inline',
            '--nopreview',
            '--sharpness', str(SHARPNESS),
            '--contrast', str(CONTRAST),
            '--brightness', str(BRIGHTNESS),
            '--denoise', 'cdn-hq',
            '--codec', 'mjpeg',
            '-o', '-'  # output to stdout
        ]
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def get_frame(self):
        # Read M-JPEG stream from rpicam-vid pipe
        # This is the most efficient way to get tuned frames on RPi 4
        bytes_data = b''
        while True:
            chunk = self.process.stdout.read(4096)
            if not chunk:
                return None, None
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8') # JPEG start
            b = bytes_data.find(b'\xff\xd9') # JPEG end
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=uint8), cv2.IMREAD_COLOR)
                return self.preprocess_frame(frame)

    def preprocess_frame(self, frame):
        if frame is None: return None, None
        
        # Grayscale for OCR processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # CLAHE (Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        return frame, enhanced

    def release(self):
        self.process.terminate()
