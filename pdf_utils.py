from fpdf import FPDF
import tempfile

# ---------------- BILL PDF ----------------
def generate_bill_pdf(patient, amount, status):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Hospital Bill", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Patient Name: {patient}", ln=True)
    pdf.cell(0, 10, f"Amount: Rs. {amount}", ln=True)
    pdf.cell(0, 10, f"Status: {status}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "Thank you for visiting our hospital.", ln=True)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)

    return file.name


# ---------------- LAB REPORT PDF ----------------
def generate_lab_report_pdf(patient, test, result):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Lab Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Patient Name: {patient}", ln=True)
    pdf.cell(0, 10, f"Test Name: {test}", ln=True)
    pdf.multi_cell(0, 10, f"Result: {result}")

    pdf.ln(10)
    pdf.cell(0, 10, "Verified by Lab Technician", ln=True)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)

    return file.name
