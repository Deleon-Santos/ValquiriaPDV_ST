import time
import streamlit as st

from services.produto_service import cadastrar_produto



def render():
    st.title("Cadastro de Produtos")

    ean = st.text_input("Código EAN")
    descricao = st.text_input("Descrição")
    preco = st.number_input("Preço", min_value=0.00, step=0.00, format="%.2f")
    estoque = st.number_input("Estoque", min_value=0, step=1)

    if st.button("Cadastrar Produto"):
        try:
            adicionado = cadastrar_produto(ean, descricao, preco, estoque)
            if adicionado == True:
                st.success("Produto cadastrado com sucesso!")
                time.sleep(2)
                st.rerun()
        except ValueError as e:
            st.error(str(e))

    st.divider()
    # st.subheader("Produtos Cadastrados")

    # for p in obter_produtos():
    #     st.write(
    #         f"EAN: {p.ean} | "
    #         f"{p.descricao} | "
    #         f"R$ {p.preco:.2f} | "
    #         f"Estoque: {p.estoque}"
    #     )
