import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

from services.produto_service import cadastrar_produto, obter_produtos


def render():
    st.title("Produtos")
    tab_add, tab_list = st.tabs(["Adicionar Produto", "Listar Produtos"])

    with tab_add:
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
                        st.rerun()

                except ValueError as e:
                    st.error(str(e))


    with tab_list:
        st.subheader("Lista de Produtos")
        produtos = obter_produtos()
        if produtos:
            df = pd.DataFrame(produtos)

            df["Preço"] = df["Preço"].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(
                resizable=True,
                sortable=True,
                filter=True
            )

            AgGrid(
                df,
                gridOptions=gb.build(),
                height=400,
                theme="balham"
            )

        else:
            st.info("Nenhum produto cadastrado.")