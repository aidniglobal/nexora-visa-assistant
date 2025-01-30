from fpdf import FPDF

def create_europass_cv(user_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Europass CV", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Name: {user_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_data['email']}", ln=True)
    
    filename = f"uploads/{user_data['name']}_europass.pdf"
    pdf.output(filename)
    return filename
