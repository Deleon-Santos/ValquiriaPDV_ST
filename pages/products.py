
import streamlit as st
from controllers.produto import cadastrar_produto, obter_produtos

def render():
    st.title("Produtos")

    name = st.text_input("Nome")
    price = st.number_input("Preço", min_value=0.0)
    stock = st.number_input("Estoque", min_value=0)

    if st.button("Cadastrar"):
        try:
            cadastrar_produto(name, price, stock)
            st.success("Produto cadastrado com sucesso")
        except ValueError as e:
            st.error(str(e))

    st.subheader("Lista de Produtos")
    for p in obter_produtos():
        st.write(f"{p.name} | R$ {p.price} | Estoque: {p.stock}")
