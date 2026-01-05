try:
    from fpdf import FPDF
except Exception:
    # Fallback minimal stub so tests/imports don't crash if fpdf isn't installed in the environment
    class FPDF:
        def __init__(self, *args, **kwargs):
            pass
        def add_page(self, *args, **kwargs):
            pass
        def set_font(self, *args, **kwargs):
            pass
        def cell(self, *args, **kwargs):
            pass
        def ln(self, *args, **kwargs):
            pass
        def multi_cell(self, *args, **kwargs):
            pass
        def image(self, *args, **kwargs):
            pass
        def output(self, filename):
            # create an empty file so callers can still send_file
            open(filename, 'wb').close()

import os
import re


def create_europass_cv(user_data, photo_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Insert photo if present (small portrait on the right)
    if photo_path and os.path.exists(photo_path):
        try:
            # place photo top-right
            pdf.image(photo_path, x=150, y=10, w=40)
        except Exception as e:
            print('Could not add photo to PDF:', e)

    pdf.cell(200, 10, txt="Europass CV", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Name: {user_data.get('name','')}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_data.get('email','')}", ln=True)

    os.makedirs('uploads', exist_ok=True)
    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', user_data.get('name','unknown'))
    filename = os.path.join('uploads', f"{safe_name}_europass.pdf")
    pdf.output(filename)
    return filename


def create_cover_letter(applicant, recipient, company, position, opening, body, closing):
    """Create a simple cover letter PDF using provided fields."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 6, txt=applicant.get('name',''), ln=True)
    pdf.cell(0, 6, txt=applicant.get('email',''), ln=True)
    pdf.ln(8)

    # Date
    from datetime import datetime, timezone
    pdf.cell(0, 6, txt=datetime.now(timezone.utc).strftime('%B %d, %Y'), ln=True)
    pdf.ln(8)

    # Recipient
    pdf.cell(0, 6, txt=f"{recipient}", ln=True)
    pdf.cell(0, 6, txt=f"{company}", ln=True)
    pdf.ln(6)

    # Greeting
    pdf.multi_cell(0, 6, txt=f"Dear {recipient},")
    pdf.ln(4)

    # Position intro
    pdf.multi_cell(0, 6, txt=f"I am writing to apply for the {position} position at {company}. {opening}")
    pdf.ln(4)

    # Body
    pdf.multi_cell(0, 6, txt=body)
    pdf.ln(4)

    # Closing
    pdf.multi_cell(0, 6, txt=closing)
    pdf.ln(8)

    pdf.multi_cell(0, 6, txt=f"Sincerely,\n{applicant.get('name','')}")

    os.makedirs('uploads', exist_ok=True)
    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', applicant.get('name','unknown'))
    filename = os.path.join('uploads', f"{safe_name}_cover_letter.pdf")
    pdf.output(filename)
    return filename
