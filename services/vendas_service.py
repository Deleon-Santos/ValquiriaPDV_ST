
from models.db import SessionLocal
from models.venda import Venda
from models.item import Venda_Item

def register_venda(cart):
    db = SessionLocal()
    total = sum(i['price']*i['qty'] for i in cart)
    sale = Venda(total=total)
    db.add(Venda_Item)
    db.commit()
    for i in cart:
        db.add(Venda_Item(sale_id=sale.id, product_id=i['id'], quantity=i['qty']))
    db.commit()
    db.close()
    return sale.id, total

# services.py


def validar_codigo(cod):
    # return buscar_produto(cod)
    pass
def criar_item(cod, qtd):
    # produto = buscar_produto(cod)
    # if not produto:
    #     return None
    pass

    # return ItemVenda(
    #     cod=cod,
    #     descricao=produto["descricao"],
    #     preco=produto["preco"],
    #     qtd=qtd
    # )
