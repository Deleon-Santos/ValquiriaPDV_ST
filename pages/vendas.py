import streamlit as st
import pandas as pd
from services.vendas_service import validar_codigo, criar_item_dto
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def render():

    # ================= ESTILO =================
    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(
                rgba(255,255,255,0.80),
                rgba(255,255,255,0.80)
            ),
            url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlvUqwmPzAC8fI3dzUfljV3ft95DuGMFY6Uw&s");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ================= FUNÇÕES =================
    def limpar_inputs():
        st.session_state.ean_input = ""
        st.session_state.qtd_input = 1

    # ================= STATE =================
    if "itens" not in st.session_state:
        st.session_state.itens = []

    if "ean_input" not in st.session_state:
        st.session_state.ean_input = ""

    if "qtd_input" not in st.session_state:
        st.session_state.qtd_input = 1

    # ================= CABEÇALHO =================
    st.header("Venda de Produtos")

    # ================= ENTRADA PRODUTO =================
    cod = st.text_input("Código EAN", key="ean_input")

    produto = None
    if cod:
        produto = validar_codigo(cod)
        if not produto:
            st.error("Produto não encontrado")

    if produto:
        qtd = st.number_input(
            "Quantidade",
            min_value=1,
            step=1,
            key="qtd_input"
        )

        if st.button("Adicionar", use_container_width=True, on_click=limpar_inputs):
            try:
                item = criar_item_dto(produto, qtd)
                st.session_state.itens.append(item)
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    # ================= DATAFRAME =================
    df = pd.DataFrame(st.session_state.itens)

    if not df.empty:
        df = df.rename(columns={
            "ean": "Código",
            "descricao": "Descrição",
            "qtd": "Qtd",
            "preco": "Preço",
            "total": "Total"
        })

    # ================= LAYOUT =================
    col_esq, col_dir = st.columns([1, 2])

    # ================= VISOR CAIXA =================
    with col_esq:

        if st.session_state.itens:
            item_atual = st.session_state.itens[-1]
            preco_unit = item_atual["preco"]
            total_item = item_atual["total"]
        else:
            preco_unit = total_item = 0.0

        total_venda = sum(i["total"] for i in st.session_state.itens)

        st.metric("Preço unitário", f"R$ {preco_unit:.2f}")
        st.metric("Total do item", f"R$ {total_item:.2f}")
        st.metric("Total da venda", f"R$ {total_venda:.2f}")

    # ================= TABELA =================
    with col_dir:

        if not df.empty:
            gb = GridOptionsBuilder.from_dataframe(df)

            gb.configure_default_column(
                resizable=True,
                sortable=False,
                filter=False,
                cellStyle={
                    "fontSize": "16px",
                    "display": "flex",
                    "alignItems": "center"
                },
            )

            gb.configure_column("Qtd", editable=True)

            grid = AgGrid(
                df,
                gridOptions=gb.build(),
                height=420,
                theme="balham",
                update_mode=GridUpdateMode.VALUE_CHANGED,
                data_return_mode="AS_INPUT",
                key="grid_vendas"
            )

            # Atualiza itens SOMENTE após edição
            if grid["data"] is not None:
                df_editado = grid["data"].copy()
                df_editado["Total"] = df_editado["Preço"] * df_editado["Qtd"]

                st.session_state.itens = [
                    {
                        "ean": row["Código"],
                        "descricao": row["Descrição"],
                        "qtd": int(row["Qtd"]),
                        "preco": float(row["Preço"]),
                        "total": float(row["Total"]),
                    }
                    for _, row in df_editado.iterrows()
                ]
        else:
            st.info("Nenhum item adicionado à venda.")
