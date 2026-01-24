import time
import streamlit as st
from services.produto_service import cadastrar_produto

def render():
    st.markdown(
        """
        <style>
        input[type="text"], input[type="number"] {color:#ffffff; background-color:white; border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius:10px; font-size: 20px;
        }
        
        
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Produtos")

    with st.form("form_produto", clear_on_submit=True):
        ean = st.text_input("Código EAN")
        descricao = st.text_input("Descrição")
        preco = st.number_input(
            "Preço", min_value=0.00, step=0.01, format="%.2f"
        )
        estoque = st.number_input(
            "Estoque", min_value=0, step=1
        )

        submitted = st.form_submit_button("Cadastrar Produto")

        if submitted:
            try:
                adicionado = cadastrar_produto(ean, descricao, preco, estoque)
                if adicionado:
                    st.success("Produto cadastrado com sucesso!")
            except ValueError as e:
                st.error(str(e))
