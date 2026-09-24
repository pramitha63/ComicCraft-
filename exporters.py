import os
from datetime import datetime
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_pdf(layout: list) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="C")
        
        y_image = 30
        image_height = 100
        image_path = os.path.join(BASE_DIR, panel['image_path'])
        
        if panel['image_path'] and os.path.exists(image_path):
            pdf.image(image_path, x=10, y=y_image, w=pdf.w - 20, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.cell(0, 10, "Image missing or pending generation", ln=True)
            
        pdf.set_y(y_image + image_height + 15)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(0, 10, panel['text'])
        
    exports_dir = os.path.join(BASE_DIR, "static", "exports")
    os.makedirs(exports_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(exports_dir, filename)
    pdf.output(pdf_path)
    return f"static/exports/{filename}"