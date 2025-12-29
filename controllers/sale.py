from services.sale_service import register_sale

def finalizar_venda(cart: list):
    if not cart:
        raise ValueError("Carrinho vazio")
    return register_sale(cart)
