
import streamlit as st
import pandas as pd
from controllers.relatorio import buscar_vendas_por_data, buscar_itens_venda
from utils.impressao import gerar_cupom_pdf

def render():
    st.markdown(
        """
        <style>
        input[type="text"], input[type="number"] {color:black; background-color:white; border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius:10px; font-size: 20px;
        }
        
        
        </style>
        """,
        unsafe_allow_html=True
    )
    st.header("🔍 Pesquisa de Vendas")

    data = st.date_input("Data da venda")

    # Inicializa estados
    if "vendas" not in st.session_state:
        st.session_state.vendas = None

    if "id_venda" not in st.session_state:
        st.session_state.id_venda = None

    # Botão pesquisar
    if st.button("Pesquisar", width="stretch"):
        vendas = buscar_vendas_por_data(data)
        st.session_state.vendas = vendas
        st.session_state.id_venda = None   # reseta seleção anterior

    # Se já temos vendas pesquisadas
    if st.session_state.vendas:
        dados = [{
            "ID Venda": v.id_venda,
            "Data": v.data_venda,
            "Total": f"R$ {v.total_venda:.2f}"
        } for v in st.session_state.vendas]

        df = pd.DataFrame(dados)

        st.dataframe(df, width="stretch", hide_index=True)

        # Selectbox persistente
        st.session_state.id_venda = st.selectbox(
            "Selecione a venda",
            options=df["ID Venda"],
            index=None if st.session_state.id_venda is None else
                   list(df["ID Venda"]).index(st.session_state.id_venda)
        )

    # Se uma venda foi selecionada
    if st.session_state.id_venda:
        itens = buscar_itens_venda(st.session_state.id_venda)

        itens_df = pd.DataFrame([{
            "n_item": item.n_item,
            "Descrição": produto.descricao,
            "EAN": produto.ean,
            "Qtd": item.qtd,
            "Unit": f"R$ {produto.preco:.2f}",
            "Total": f"R$ {item.total:.2f}",
            "Valor Venda": f"R$ {venda.total_venda:.2f}"
        } for item, produto, venda in itens])

        st.subheader("🧾 Itens da Venda")
        st.dataframe(itens_df, width="stretch")

        if st.button("🖨 Imprimir Cupom", width="stretch"):
            arquivo = gerar_cupom_pdf(st.session_state.id_venda, itens)
            st.success(f"Cupom gerado: {arquivo}")
