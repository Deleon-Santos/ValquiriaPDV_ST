from services.vendas_service import register_venda

def finalizar_venda(cart: list):
    if not cart:
        raise ValueError("Carrinho vazio")
    return register_venda(cart)
