from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def gerar_cupom_pdf(id_venda,dados_venda, itens): 
    largura_cupom = 80 * mm
    altura_estimada = 150 * mm + (len(itens) * 5 * mm) # Dinâmico
    
    nome_arquivo = f"cupom_venda_{id_venda}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=(largura_cupom, altura_estimada))
    
    # Coordenadas iniciais
    largura = largura_cupom
    y = altura_estimada - 10 * mm
    margem_esquerda = 5 * mm
    margem_direita = largura - 5 * mm
    centro = largura / 2

    # --- Cabeçalho ---
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(centro, y, "SUPERMERCADO VALQUÍRIA")
    y -= 12
    
    c.setFont("Helvetica", 8)
    c.drawCentredString(centro, y, "Rua das Flores de marco, 12300 - Centro")
    y -= 12
    c.drawCentredString(centro, y, "Telefone: (11) 0000-0000")
    y -= 12

    venda = itens[0][2]
    data_str = venda.data_venda.strftime("%d/%m/%Y %H:%M")
    
    c.setFont("Helvetica", 7)
    c.drawString(margem_esquerda, y, f"Cupom: {venda.id_venda:06d}")
    c.drawRightString(margem_direita, y, data_str)
    y -= 8

    # --- Cabeçalho da Tabela ---
    c.line(margem_esquerda, y, margem_direita, y)
    y -= 8
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margem_esquerda, y, "Item")
    c.drawString(12 * mm, y, "Desc/ean")
    c.drawString(49 * mm, y, "Preço/qtd")
    c.drawRightString(margem_direita, y, "Total")
    y -= 4
    c.line(margem_esquerda, y, margem_direita, y)
    y -= 8

    # --- Itens ---
    c.setFont("Helvetica", 7)
    for item, produto, venda_obj in itens:
        # Descrição do produto (Truncada para caber)
        desc = produto.descricao[:25]
        c.drawString(margem_esquerda, y, f"{item.id_item_venda:03d}") # Código
        c.drawString(margem_esquerda + 7*mm, y, desc)
        c.drawRightString(60*mm, y, f"{produto.preco:.2f}")
        y -= 8
        
        # Valores na linha debaixo ou alinhados (estilo cupom)
        
        c.drawRightString(margem_esquerda + 55*mm, y, f"x{item.qtd}")
        c.drawString(margem_esquerda + 7*mm, y, produto.ean)
        c.drawRightString(margem_direita, y, f"{item.total:.2f}")
        y -= 8

        if y < 15 * mm: # Margem de segurança inferior
            c.showPage()
            y = altura_estimada - 10 * mm
            c.setFont("Helvetica", 7)

    # --- Totalizadores ---
    y -= 8
    c.line(margem_esquerda, y, margem_direita, y)
    y -= 12
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esquerda, y, "TOTAL R$")
    c.drawRightString(margem_direita, y, f"{float(dados_venda['Total']):.2f}")
    y -= 8

    c.setFont("Helvetica", 7)
    c.drawString(margem_esquerda, y - 12, f"Forma de Pagamento: {dados_venda['Forma Pagamento'].capitalize()}")
    if dados_venda['Forma Pagamento'] == "dinheiro":
        c.drawString(margem_esquerda, y - 24, f"Valor recebido: R$ {float(dados_venda['Total']):.2f}")
        c.drawString(margem_esquerda, y - 36, f"Troco: R$ {float(dados_venda['Troco']):.2f}")   
    y -= 4
    c.line(margem_esquerda, y, margem_direita, y)
    y -= 8
    c.drawString(margem_esquerda, y - 12, f"Atendente: {dados_venda['ID Usuario']}")   

    # --- Rodapé ---
    y -= 40
    c.setFont("Helvetica", 7)
    c.drawCentredString(centro, y, "Obrigado pela preferência!")
    y -= 8
    c.drawCentredString(centro, y, "Sistema PDV - Projeto Valquíria")

    c.save()
    return nome_arquivo