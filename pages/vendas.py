from time import sleep, time
import streamlit as st
import pandas as pd
# from controllers.produto import buscar_produto_por_descricao
from controllers.vendas import iniciar_venda
# from pages.pesquisa import abrir_modal
from services.vendas_service import criar_item_dto, remover_item
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode



def render():
    usuario = st.session_state.usuario_logado
    id_venda = iniciar_venda(usuario)
    print(id_venda)
    # ================= ESTILO =================
    st.markdown(
        """
        <style>
        input[type="text"], input[type="number"] {color:ffff; background-color:white; border:1px solid black;border-radius:10px; font-size: 30rpx;backgound-color: silver;
        }
        .stApp {
            backgoround-color:light-blue
            }
        # .stApp {
        #     background-image: linear-gradient(
        #         rgba(255,255,255,0.80),
        #         rgba(255,255,255,0.80)
        #     ),
        #     # url("https://img.freepik.com/fotos-gratis/abundancia-de-escolhas-de-alimentos-saudaveis-no-corredor-do-supermercado-geradas-pela-ia_188544-42447.jpg?semt=ais_hybrid&w=740&q=80");
        #     background-size: cover;
        #     background-position: center;
        #     background-repeat: no-repeat;
        #     background-attachment: fixed;
        # }
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
    with col_dir:
        item_selecionado = None

        st.markdown(
            f"""
            <div style="text-align: right; font-size: 15px; font-weight: bold; padding-bottom:5px;border-bottom:0px;">
                Cupom: {id_venda:04d}
            </div>
            """,
            unsafe_allow_html=True
        )

        if not df.empty:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(selection_mode="single", use_checkbox=True)
            # 🔒 TODAS AS COLUNAS BLOQUEADAS
            gb.configure_default_column(
                resizable=True,
                sortable=False,
                filter=False,
                editable=False,
                cellStyle={
                    "fontSize": "16px",
                    "display": "flex",
                    "alignItems": "center"
                },
            )

            # 💰 FORMATAÇÃO MONETÁRIA (VISUAL)
            gb.configure_columns(
                ["Preço", "Total"],
                type=["numericColumn"],
                valueFormatter="""
                    function(params) {
                        if (params.value === null || params.value === undefined) {
                            return '';
                        }
                        return Number(params.value).toLocaleString(
                                'pt-BR',
                                { minimumFractionDigits: 2, maximumFractionDigits: 2 }
                        );
                    }
                """,
                cellStyle={"textAlign": "right"}
            )

            grid_response = AgGrid(
                df,
                gridOptions=gb.build(),
                height=370,
                theme="balham",
                update_mode=GridUpdateMode.SELECTION_CHANGED, # Garante que o Streamlit saiba quando selecionamos algo
                key="grid_vendas"
            )
            
            # Pegar o item selecionado
            item_selecionado = grid_response['selected_rows']
            print(item_selecionado)
        else:
            st.info("Nenhum item adicionado à venda.")
            item_selecionado = None

    with col_esq:
        
        
        try:
            
            # produto = None
            codigo = st.text_input("Código EAN", key="ean_input")
            # cod= codigo
                      
            col01, col02 = st.columns([2,1])
            with col01:
                quantid = st.number_input(
                "Quantidade",
                min_value=1,
                step=1,
                key="qtd_input"
            )
                if st.button("Add Item", use_container_width=True):
                    item = criar_item_dto(codigo, quantid, id_venda)
                    print(item)
                    if item:
                        st.session_state.itens=item

                        # apenas sinaliza
                        st.session_state.limpar_inputs = True

                        st.rerun()
                    else:
                        st.error("Produto não foi localizado")
                
                
            # qtd = quantid
            with col02:
                st.markdown(
                    f"<div style='text-align:left; font-size:14px;padding-bottom:5px; margin-top:0'>Excluir</div>",
                    unsafe_allow_html=True
                )
                
                if st.button("Del Item", use_container_width=True):
                    # LÓGICA DE EXCLUSÃO
                    if item_selecionado is not None:
                        try:
                            # Se for DataFrame, usa iloc
                            if isinstance(item_selecionado, pd.DataFrame) and not item_selecionado.empty:
                                id_para_excluir = int(item_selecionado['item'].iloc[0])
                                print(f"lista de item para excluir {id_para_excluir}")
                                removido = remover_item(id_para_excluir, id_venda)
                                if removido == True:
                                    print("item removido ")
                                    st.rerun()
                                    
                                else:
                                    print("item nao foi enconrado no banco de dados")
                                        # Se for lista, usa índice
                            else:
                               
                                print(f"item para excluir não localizado na lista de iten do df {id_para_excluir}")
                                
                            # Chama a função de remoção
                            
                            
                        except Exception as e:
                            st.error(f"Erro ao capturar item: {e}")
                            
                    else:
                        print("o item selecionado não foi encontrado")
                    
                
                if st.button("Buscar", use_container_width=True):
                   pass
                    # st.session_state.abrir_modal = True
                    

                
                #implementar a regra para deletar itens
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

        # st.text_input(
        #     "Preço unitário",
        #     value=f"R$ {preco_unit:.2f}",
        #     disabled=True
        # )

        # st.text_input(
        #     "Total do item",
        #     value=f"R$ {total_item:.2f}",
        #     disabled=True
        # )
        st.markdown(
            f"<div style='text-align:left; font-size:14px;padding-bottom:10px'>Preço Unitario R$</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div style='text-align:right; font-size:20px;border:1px solid black; border-radius: 10px; background-color: light-silver; padding:10px'> {preco_unit:.2f}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='text-align:left; font-size:14px;padding:10px 0'>Total R$</div>",
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"<div style='text-align:right; font-size:20px;border:1px solid black; border-radius: 10px; background-color: light-silver; padding:10px; margin-bottom:20px'> {total_item:.2f}</div>",
            unsafe_allow_html=True
        )


        

    # ================= TABELA =================
    
   





    col1 , col2 = st.columns([3,1])
    with col1:
        # st.markdown(
        #     "<div style='text-align:left; font-size:24px; font-weight:bold;'>Descrição</div>",
        #     unsafe_allow_html=True
        # )
        st.markdown(
        f"<div style='text-align:left; font-size:40px; border:1px solid black; border-radius: 10px; background-color: silver ;padding:10px'>{desc_item}</div>",
        unsafe_allow_html=True
    )

    with col2:
        # st.markdown(
        #     "<div style='text-align:right; font-size:24px; font-weight:bold;'>Total da Venda R$</div>",
        #     unsafe_allow_html=True
        # )
        st.markdown(
            f"<div style='text-align:right; font-size:40px;border:1px solid black; border-radius: 10px; background-color: silver; padding:10px'> {total_venda:.2f}</div>",
            unsafe_allow_html=True
        )
