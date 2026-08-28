from fpdf import FPDF
import datetime
import os
from config import CHALLANS_DIR

class ChallanGenerator:
    def __init__(self):
        if not os.path.exists(CHALLANS_DIR):
            os.makedirs(CHALLANS_DIR)

    def generate(self, plate_number, violation_type, image_path):
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", "B", 24)
        pdf.cell(200, 20, "TRAFFIC VIOLATION CHALLAN", ln=True, align="C")
        pdf.ln(10)
        
        # Details
        pdf.set_font("Arial", "", 14)
        pdf.cell(200, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(200, 10, f"Plate Number: {plate_number}", ln=True)
        pdf.cell(200, 10, f"Violation: {violation_type}", ln=True)
        pdf.cell(200, 10, f"Location: Sentinel Zone A", ln=True)
        pdf.ln(10)
        
        # Evidence Image
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=80, w=180)
            
        filename = f"challan_{plate_number}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(CHALLANS_DIR, filename)
        pdf.output(file_path)
        
        print(f"Challan PDF generated: {file_path}")
        return file_path
