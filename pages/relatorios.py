
import streamlit as st
import pandas as pd
from controllers.relatorio import buscar_vendas_por_data, buscar_itens_venda
from utils.impressao import gerar_cupom_pdf


def render():
    st.header("🔍 Pesquisa de Vendas")
    data1, data2 = st.columns(2)
    with data1:
        data_inicio = st.date_input("Data inicio")
    with data2:
        data_fim = st.date_input("Data fim")

    # Inicializa estados
    if "vendas" not in st.session_state:
        st.session_state.vendas = None

    if "id_venda" not in st.session_state:
        st.session_state.id_venda = None

    if st.button("Pesquisar", width="stretch"):
        vendas = buscar_vendas_por_data(data_inicio, data_fim)
        st.session_state.vendas = vendas
        st.session_state.id_venda = None   

    # Se já temos vendas pesquisadas
    if st.session_state.vendas:
        dados = [{
            "ID Venda": v.id_venda,
            "Data": v.data_venda,
            "Total": f"{v.total_venda:.2f}",
            "Valor Pago" : f"{v.valor_pago:.2f}",
            "Troco" : f"{v.troco:.2f}",
            "Forma Pagamento" : v.forma_pagamento,
            "Status" : v.status,
            "ID Usuario" : v.id_usuario
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
        dados_venda = [v for v in dados
                        if v["ID Venda"] == st.session_state.id_venda][0]
        #print(dados_venda)
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
            arquivo = gerar_cupom_pdf(st.session_state.id_venda, dados_venda, itens)
            st.success(f"Cupom gerado: {arquivo}")
            if arquivo:
                with open(arquivo, "rb") as file:
                    st.download_button(
                        label="📥 Baixar Cupom",
                        data=file,
                        file_name="cupom.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
