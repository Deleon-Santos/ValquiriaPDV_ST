from services.product_service import create_product, list_products

def cadastrar_produto(name: str, price: float, stock: int):
    if not name or price <= 0 or stock < 0:
        raise ValueError("Dados inválidos")
    create_product(name, price, stock)

def obter_produtos():
    return list_products()
