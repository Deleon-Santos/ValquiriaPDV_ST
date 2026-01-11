
import streamlit as st
from controllers.vendas import criar_item
# from db import db
from db.db import SessionLocal
from models.models import Venda , Produto, Item_Venda

    
def criar_item_dto(cod: str, qtd: int, id_venda) -> list[dict]:
    cod=cod.strip()
    usuario = st.session_state.usuario_logado
    novo_item=criar_item(cod, qtd, usuario)

    session = SessionLocal()

    
    try:
        itens = (
        session.query(Item_Venda)
        .join(Produto)
        .filter(Item_Venda.id_venda == id_venda)
        .all()
        )

        return [
            {
            "id_item": item.id_item_venda,
            "ean": item.produto.ean,
            "descricao": item.produto.descricao,
            "qtd": item.qtd,
            "preco": item.produto.preco,
            "total": item.total
        }
        for item in itens
    ]

    finally:
        session.close()

