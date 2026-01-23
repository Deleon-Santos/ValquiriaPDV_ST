from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def gerar_cupom_pdf(id_venda, itens):
    nome_arquivo = f"cupom_venda_{id_venda}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)

    largura, altura = A4
    y = altura - 50

    # Cabeçalho
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(largura / 2, y, "SUPERMERCADO VALQUÍRIA")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawCentredString(largura / 2, y, "CUPOM FISCAL SIMPLIFICADO")
    y -= 30

    # Dados da venda
    venda = itens[0][2]
    data_str = venda.data_venda.strftime("%d/%m/%Y %H:%M")

    c.drawString(50, y, f"Venda Nº: {venda.id_venda}")
    y -= 15
    c.drawString(50, y, f"Data: {data_str}")
    y -= 25

    # Cabeçalho da tabela
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Item")
    c.drawString(90, y, "Descrição")
    c.drawString(300, y, "Qtd")
    c.drawString(340, y, "Unit")
    c.drawString(400, y, "Total")
    y -= 10

    c.line(50, y, 550, y)
    y -= 15

    # Itens da venda
    c.setFont("Helvetica", 9)

    for item, produto, venda in itens:
        c.drawString(50, y, str(item.id_item_venda))   # ou outro campo identificador
        c.drawString(90, y, produto.descricao[:30])
        c.drawString(300, y, str(item.qtd))
        c.drawString(340, y, f"{produto.preco:.2f}")
        c.drawString(400, y, f"{item.total:.2f}")
        y -= 15

        # Quebra de página se necessário
        if y < 100:
            c.showPage()
            y = altura - 50
            c.setFont("Helvetica", 9)

    # Linha final
    y -= 10
    c.line(50, y, 550, y)
    y -= 25

    # Total da venda
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(550, y, f"TOTAL: R$ {venda.total_venda:.2f}")
    y -= 40

    # Rodapé
    c.setFont("Helvetica", 9)
    c.drawCentredString(largura / 2, y, "Obrigado pela preferência!")
    y -= 15
    c.drawCentredString(largura / 2, y, "Sistema PDV - Projeto Valquíria")

    c.save()

    return nome_arquivo
