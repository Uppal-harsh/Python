import cv2
import numpy as np
import easyocr
from config import PLATE_RESIZE_DIM

class OCRManager:
    def __init__(self):
        # Initialize EasyOCR (English)
        # Note: First run will download model weights (~30MB)
        self.reader = easyocr.Reader(['en'], gpu=False) # RPi doesn't have GPU for this
        
    def enhance_plate(self, plate_crop):
        """Pre-OCR enhancement for the cropped plate region"""
        # Resize to standard size
        plate = cv2.resize(plate_crop, PLATE_RESIZE_DIM)
        
        # Convert to grayscale if not already
        if len(plate.shape) == 3:
            gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        else:
            gray = plate
            
        # Apply CLAHE for contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Sharpen
        sharpen_kernel = np.array([[-1,-1,-1],
                                    [-1, 9,-1],
                                    [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, sharpen_kernel)
        
        # Otsu Thresholding
        _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh

    def read_plate(self, plate_crop):
        processed_plate = self.enhance_plate(plate_crop)
        results = self.reader.readtext(processed_plate)
        
        # Extract text and filter out low confidence / short strings
        plate_text = ""
        for (bbox, text, prob) in results:
            # Simple alphanumeric filtering (removes noise)
            clean_text = "".join([c for c in text if c.isalnum()]).upper()
            if len(clean_text) > 4: # Typical plate length minimum
                plate_text = clean_text
                break
                
        return plate_text, processed_plate
