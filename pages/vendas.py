import streamlit as st
import pandas as pd
from controllers.vendas import iniciar_venda
from services.vendas_service import criar_item_dto
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def render():
    usuario = st.session_state.usuario_logado
    id_venda = iniciar_venda(usuario)
    print(id_venda)
    # ================= ESTILO =================
    st.markdown(
        """
        <style>
        input[type="text"], input[type="number"] {color:black; background-color:white; border:1px solid black;
        }
        .stApp {
            background-image: linear-gradient(
                rgba(255,255,255,0.80),
                rgba(255,255,255,0.80)
            ),
            url("https://img.freepik.com/fotos-gratis/abundancia-de-escolhas-de-alimentos-saudaveis-no-corredor-do-supermercado-geradas-pela-ia_188544-42447.jpg?semt=ais_hybrid&w=740&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

  
   
    if "itens" not in st.session_state:
        st.session_state.itens = []

    if "ean_input" not in st.session_state:
        st.session_state.ean_input = ""

    if "qtd_input" not in st.session_state:
        st.session_state.qtd_input = 1

   
    df = pd.DataFrame(st.session_state.itens)
    
    if not df.empty:
        df = df.rename(columns={
            "id_item": "item",
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
        
        #col1, col2 = st.columns([1,2])
        try:
            
            # produto = None
            codigo = st.text_input("Código EAN", key="ean_input")
            cod= codigo
            print(cod)
            quantid = st.number_input(
                "Quantidade",
                min_value=1,
                step=1,
                key="qtd_input"
            )
            qtd = quantid
            if st.button("Adicionar", use_container_width=True):
                item = criar_item_dto(codigo, quantid, id_venda)
                print(item)
                if item:
                    st.session_state.itens=item

                    # apenas sinaliza
                    st.session_state.limpar_inputs = True

                    st.rerun()
                else:
                    st.error("Produto não foi localizado")

        except ValueError as e:
            st.error(str(e))





# __________________________________________________________________________________________________________________

        if st.session_state.itens:
            item_atual = st.session_state.itens[-1]
            preco_unit = item_atual["preco"]
            total_item = item_atual["total"]
            desc_item = item_atual["descricao"]
        else:
            preco_unit = total_item = 0.0
            desc_item = ""

        total_venda = sum(i["total"] for i in st.session_state.itens)

        st.text_input(
            "Preço unitário",
            value=f"R$ {preco_unit:.2f}",
            disabled=True
        )

        st.text_input(
            "Total do item",
            value=f"R$ {total_item:.2f}",
            disabled=True
        )

        

    # ================= TABELA =================
    with col_dir:
        st.markdown(
            f"""
            <div style="text-align: right; font-size: 20px; font-weight: bold;">
                Cupom: {id_venda:04d}
            </div>
            """,
            unsafe_allow_html=True
        )

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
                        "item": row['item'],
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
    col1 , col2 = st.columns([3,1])
    with col1:
        st.markdown(
            "<div style='text-align:left; font-size:24px; font-weight:bold;'>Descrição</div>",
            unsafe_allow_html=True
        )
        st.markdown(
        f"<div style='text-align:left; font-size:40px; border:1px solid black; border-radius: 10px; background-color: silver ;padding:10px'>{desc_item}</div>",
        unsafe_allow_html=True
    )


    with col2:
        st.markdown(
            "<div style='text-align:right; font-size:24px; font-weight:bold;'>Total da Venda R$</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='text-align:right; font-size:40px;border:1px solid black; border-radius: 10px; background-color: silver; padding:10px'> {total_venda:.2f}</div>",
            unsafe_allow_html=True
        )
