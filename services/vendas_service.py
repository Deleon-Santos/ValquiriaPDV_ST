import streamlit as st
from controllers.vendas import carrinho_atual, criar_item, delete_item, iniciar_venda
from controllers.produto import buscar_produto_por_descricao


    
def criar_item_dto(cod: str, qtd: int, id_venda: int) -> list[dict]:   
    cod=cod.strip()
    return criar_item(cod, qtd, id_venda)


def remover_item(n_item: int, id_venda: int):   
    item_deletado = delete_item(n_item , id_venda)
    if item_deletado ==True:
        return carrinho_atual(id_venda)


def buscar_descricao(pesquisa_descricao):
    return (buscar_produto_por_descricao(pesquisa_descricao))


def pegar_n_venda_atual(usuario: dict):
    return iniciar_venda(usuario)


def atualizar_tabela(id_venda: int):
    return carrinho_atual(id_venda)