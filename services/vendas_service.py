
from models import db
from models.db import SessionLocal
from models.venda import Venda
from models.item import Venda_Item
from models.produto import Product



def validar_codigo(cod):
    db = SessionLocal()
    
    try:
        produto = db.query(Product).filter(Product.cod == cod).first()
        return produto
    finally:
        db.close()



def criar_item(produto, qtd):
    return Venda_Item(
        cod=produto.cod,
        descricao=produto.name,
        preco=produto.preco,
        qtd=qtd,
        total=produto.preco * qtd
    )

def register_venda(cart):
    # db = SessionLocal()
    # try:
    #     total = sum(i["preco"] * i["qtd"] for i in cart)

    #     venda = Venda(total=total)
    #     db.add(venda)
    #     db.commit()
    #     db.refresh(venda)

    #     for item in cart:
    #         db.add(
    #             Venda_Item(
    #                 sale_id=venda.id,
    #                 product_id=item["id"],
    #                 quantity=item["qtd"]
    #             )
    #         )

    #     db.commit()
    #     return venda.id, total
    # finally:
    #     db.close()
    pass