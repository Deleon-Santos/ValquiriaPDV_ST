import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.relatorio import buscar_vendas_por_data, buscar_itens_venda
from utils.impressao import gerar_cupom_pdf


def render():
    st.header("Pesquisa de Vendas")
    tab1, tab2 = st.tabs(["Dashboard de Vendas", "Relatório Completo"])

    with tab1:
         
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
            "Valor recebido" : f"{v.valor_pago:.2f}",
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

        st.subheader("Itens da Venda")
        st.dataframe(itens_df, width="stretch")
        try:
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
        except Exception as e:
            st.error("Erro ao gerar cupom: Venda Aberta!")
    

    with tab2:

        st.set_page_config(layout="wide")

        st.subheader("Dashboard de Vendas")

       
        # col1, col2 = st.columns(2)

        # with col1:
        #     data_inicio = st.date_input("Data início")

        # with col2:
        #     data_fim = st.date_input("Data fim")

        vendas = buscar_vendas_por_data(data_inicio, data_fim)

        vendas_pag = [v for v in vendas if v.status.lower() == "pago"]

        if not vendas_pag:
            st.warning("Nenhuma venda encontrada.")
            return

       
        total_vendido = sum(v.total_venda for v in vendas_pag)
        qtd_vendas = len(vendas_pag)
        ticket_medio = total_vendido / qtd_vendas if qtd_vendas else 0

        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric("💰 Total Vendido", f"R$ {total_vendido:,.2f}")
        kpi2.metric("🧾 Nº de Vendas", qtd_vendas)
        kpi3.metric("📈 Ticket Médio", f"R$ {ticket_medio:,.2f}")

        st.divider()

        aba1, aba2 = st.tabs(["📈 Vendas por Dia", "🍕 Produtos"])

       
        with aba1:

            df_vendas = pd.DataFrame([{
                "data": v.data_venda,
                "total": float(v.total_venda)
            } for v in vendas_pag])

            df_vendas["data"] = pd.to_datetime(df_vendas["data"]).dt.date

            df_agrupado = df_vendas.groupby("data")["total"].sum().reset_index()

            fig = px.line(
                df_agrupado,
                x="data",
                y="total",
                markers=True,
                title="Evolução das Vendas"
            )

            st.plotly_chart(fig, use_container_width=True)

        
        with aba2:

            itens_lista = []

            for venda in vendas_pag:
                itens = buscar_itens_venda(venda.id_venda)

                for item, produto, _ in itens:
                    itens_lista.append({
                        "produto": produto.descricao,
                        "quantidade": item.qtd
                    })

            df_itens = pd.DataFrame(itens_lista)

            if df_itens.empty:
                st.warning("Sem itens.")
                return

            df_top = df_itens.groupby("produto")["quantidade"].sum().reset_index()

            
            df_top = df_top.sort_values(by="quantidade", ascending=False).head(5)

            fig_pizza = px.pie(
                df_top,
                names="produto",
                values="quantidade",
                title="Top 5 Produtos Mais Vendidos",
                hole=0.4  # estilo donut (mais moderno)
            )

            st.plotly_chart(fig_pizza, use_container_width=True)