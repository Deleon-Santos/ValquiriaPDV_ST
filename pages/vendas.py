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
        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            border: 1.5px solid #cfcfcf !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 2.1rem !important;
            text-align: right !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Venda Produto")

    # ================= STATE =================
    if "itens" not in st.session_state:
        st.session_state.itens = []

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
            value=1,
            key="qtd_input"
        )

        if st.button("Adicionar", use_container_width=True):
            try:
                item = criar_item_dto(produto, qtd)
                st.session_state.itens.append(item)
                st.session_state.ean_input = ""
                st.session_state.qtd_input = 1
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    # ================= DATAFRAME =================
    df = pd.DataFrame(
        st.session_state.itens,
        columns=["ean", "descricao", "qtd", "preco", "total"]
    ).rename(columns={
        "ean": "Código",
        "descricao": "Descrição",
        "qtd": "Qtd",
        "preco": "Preço",
        "total": "Total"
    })

    col_esq, col_dir = st.columns([1, 2])

    # ================= VISOR CAIXA =================
    with col_esq:

        if st.session_state.itens:
            item_atual = st.session_state.itens[-1]
            preco_unit = item_atual["preco"]
            qtd_item = item_atual["qtd"]
            total_item = item_atual["total"]
        else:
            preco_unit = total_item = 0.0

        total_venda = sum(i["total"] for i in st.session_state.itens)

        st.markdown("### Preço unitário")
        st.text_input("", f"{preco_unit:.2f}", disabled=True)

        st.markdown("### Total do item")
        st.text_input("", f"{total_item:.2f}", disabled=True)

        st.markdown("### Total da venda")
        st.text_input("", f"{total_venda:.2f}", disabled=True)

    # ================= TABELA =================
    with col_dir:

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

        df_editado = grid["data"]
        df_editado["Total"] = df_editado["Preço"] * df_editado["Qtd"]

        # 🔄 Atualiza session_state SEM ORM
        st.session_state.itens = [
            {
                "id_produto": row.get("id_produto"),
                "ean": row["Código"],
                "descricao": row["Descrição"],
                "qtd": int(row["Qtd"]),
                "preco": float(row["Preço"]),
                "total": float(row["Total"]),
            }
            for _, row in df_editado.iterrows()
        ]
