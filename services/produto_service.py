from controllers.produto import criar_produto, listar_produtos


def cadastrar_produto(ean: str, descricao: str, preco: float, estoque: int):

    if not ean or not descricao:
        raise ValueError("EAN e descrição são obrigatórios")

    if preco <= 0:
        raise ValueError("Preço deve ser maior que zero")

    if estoque < 0:
        raise ValueError("Estoque inválido")
    descricao = descricao.title()
    return criar_produto(ean, descricao, preco, estoque)
    



def obter_produtos():
    return listar_produtos()
