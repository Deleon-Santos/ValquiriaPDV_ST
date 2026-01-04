import streamlit as st
import pandas as pd
from services.vendas_service import validar_codigo, criar_item
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def render():

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

 
    # GARANTE que existe carrinho
    if "itens" not in st.session_state:
        st.session_state.itens = []

    # 🔹 DATAFRAME SEMPRE EXISTE (MESMO VAZIO)
        df = pd.DataFrame(
            [
                {
                    "Código": i.cod,
                    "Descrição": i.descricao,
                    "Qtd": i.qtd,
                    "Preço": i.preco,
                    "Total": i.total,
                }
                for i in st.session_state.itens
            ],
            columns=["Código", "Descrição", "Qtd", "Preço", "Total"]
        )


   

    col_esq, col_dir = st.columns([1, 2])

# ================= COLUNA ESQUERDA =================
    with col_esq:
        

        cod = st.text_input("Código EAN")

        if cod:
            produto = validar_codigo(cod)
            if produto:
                st.success(f"Produto: {produto['descricao']}")
                st.session_state.produto_encontrado = produto
            else:
                st.error("Produto não encontrado")

        # ===== CAMPOS DE VALORES (VISOR DO CAIXA) =====
        

        # Item atual
        if st.session_state.itens:
            item_atual = st.session_state.itens[-1]
            preco_unit = item_atual.preco
            qtd_item = item_atual.qtd
            total_item = preco_unit * qtd_item
        else:
            preco_unit = 0.0
            total_item = 0.0

        total_venda = sum(i.total for i in st.session_state.itens)

        st.markdown("### Preço unitário")
        st.text_input(
            label="Preço unitário",
            value=preco_unit,
            disabled=True,
            label_visibility="collapsed",key="preco_unitario"
        )

        st.markdown("### Total do item")
        st.text_input(
            label="Total do item",
            value=total_item,
            disabled=True,
            label_visibility="collapsed",key="total_item"
        )

        st.markdown("### Total da venda")
        st.text_input(
            label="Total da venda",
            value=total_venda,
            disabled=True,
            label_visibility="collapsed",key="valor_total"
        )

# ================= COLUNA DIREITA =================
   # ================= COLUNA DIREITA =================
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

        gb.configure_column(
            "Código",
            width=120,
            cellStyle={"textAlign": "right"}
        )

        gb.configure_column(
            "Descrição",
            width=320,
            cellStyle={"textAlign": "left"}
        )

        gb.configure_column(
            "Preço",
            width=110,
            type=["numericColumn"],
            valueFormatter="value.toLocaleString('pt-BR', {minimumFractionDigits: 2})",
            cellStyle={"textAlign": "right"}
        )

        gb.configure_column(
            "Qtd",
            width=80,
            editable=True,
            cellStyle={"textAlign": "right"}
        )

        gb.configure_column(
            "Total",
            width=130,
            type=["numericColumn"],
            valueFormatter="value.toLocaleString('pt-BR', {minimumFractionDigits: 2})",
            cellStyle={"textAlign": "right", "fontWeight": "bold"}
        )

        gb.configure_column("Código", width=200)
        gb.configure_column("Descrição", width=600)
        gb.configure_column("Qtd", width=200, editable=True)
        gb.configure_column("Preço", width=200)
        gb.configure_column("Total", width=200)

        grid_options = gb.build()

        AgGrid(
            df,
            gridOptions=grid_options,
            height=420,
            fit_columns_on_grid_load=True,
            theme="balham",
            key="grid_vendas"
        )
