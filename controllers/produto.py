from services.produtos_service import create_product, list_products

def cadastrar_produto(cod: str,name: str, preco: float):
    if not name or preco <= 0 or not cod:
        raise ValueError("Dados inválidos")
    create_product(cod,name,preco)

def obter_produtos():
    return list_products()
