
import streamlit as st
from controllers.produto import cadastrar_produto, obter_produtos

def render():
    st.title("Cadastro de Produtos")
    cod = st.text_input("cod/ean")
    name = st.text_input("Descrição")
    price = st.number_input("Preço", min_value=0.0)
    

    if st.button("Cadastrar"):
        try:
            cadastrar_produto(cod, name, price)
            st.success("Produto cadastrado com sucesso")
        except ValueError as e:
            st.error(str(e))

    st.subheader("Lista de Produtos")
    for p in obter_produtos():
        st.write(f"Cod: {p.cod}| nome: {p.name} | R$ {p.price} ")
