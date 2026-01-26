import streamlit as st
from controllers.vendas import carrinho_atual, criar_item, delete_item
from db.db import SessionLocal
from models.models import Produto, Item_Venda

    
def criar_item_dto(cod: str, qtd: int, id_venda) -> list[dict]:
    cod=cod.strip()
    usuario = st.session_state.usuario_logado
    criar_item(cod, qtd, usuario)
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
            "id_item": item.n_item,
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


def remover_item(n_item: int, id_venda: int):
    
    item_deletado = delete_item(n_item , id_venda)
    if item_deletado ==True:
        return carrinho_atual(id_venda)
    
    