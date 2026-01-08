
from typing import List
from db import db
from db.db import SessionLocal
from models.models import Venda , Produto, Item_Venda





def validar_codigo(cod: str) -> Produto | None:
    session = SessionLocal()
    try:
        return session.query(Produto).filter(Produto.ean == cod).first()
    finally:
        session.close()




def criar_item(produto: Produto, qtd: int) -> Item_Venda:
    
    return Item_Venda(

        ean=produto.ean,
        descricao=produto.descricao,
        preco=produto.preco,
        qtd=qtd,
        total=produto.preco * qtd
    )

def criar_item_dto(produto: Produto, qtd: int) -> dict:
    if produto.estoque < qtd:
        raise ValueError("Estoque insuficiente")

    return {
        "id_produto": produto.id_produto,
        "ean": produto.ean,
        "descricao": produto.descricao,
        "qtd": qtd,
        "preco": produto.preco,
        "total": produto.preco * qtd
    }


def register_venda(
    itens: List[Item_Venda],
    id_usuario: int | None = None
) -> tuple[int, float]:

    session = SessionLocal()

    try:
        # Recarrega produtos com lock lógico
        for item in itens:
            produto = session.query(Produto).get(item.id_produto)

            if produto.estoque < item.qtd:
                raise ValueError(
                    f"Estoque insuficiente para {produto.descricao}"
                )

            produto.estoque -= item.qtd

        total_venda = sum(item.total for item in itens)

        venda = Venda(
            total_venda=total_venda,
            id_usuario=id_usuario,
            itens=itens  # relacionamento faz o resto
        )

        session.add(venda)
        session.commit()

        return venda.id_venda, total_venda

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
