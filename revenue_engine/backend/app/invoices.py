from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_invoice_pdf(invoice_number: str, customer_name: str, amount_inr: int) -> bytes:
    out = BytesIO(); c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"Invoice {invoice_number}")
    c.drawString(50, 800, "Amravati Revenue Engine")
    c.drawString(50, 775, f"Invoice: {invoice_number}")
    c.drawString(50, 750, f"Customer: {customer_name}")
    c.drawString(50, 725, f"Total: INR {amount_inr:,.2f}")
    c.drawString(50, 690, "Payment status must be based on verified reconciliation.")
    c.save(); return out.getvalue()
