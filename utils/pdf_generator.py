
from reportlab.pdfgen import canvas

def generate_pdf(sale_id, total):
    c = canvas.Canvas(f"cupom_{sale_id}.pdf")
    c.drawString(100,750,f"Venda #{sale_id}")
    c.drawString(100,730,f"Total: R$ {total}")
    c.save()
