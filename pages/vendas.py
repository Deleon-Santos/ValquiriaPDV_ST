
import time
import streamlit as st
import pandas as pd


from services.vendas_service import atualizar_tabela, buscar_descricao, criar_item_dto, pegar_n_venda_atual, remover_item
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def render():
    # configurações iniciais
    usuario = st.session_state.usuario_logado
    id_venda = pegar_n_venda_atual(usuario)
    venda, pesquisa = st.tabs(["Venda", "Pesquisa"])

    st.session_state.itens = atualizar_tabela(id_venda)
    if "itens" not in st.session_state:
        st.session_state.itens = []

    if "ean_input" not in st.session_state:
        st.session_state.ean_input = ""

    if "qtd_input" not in st.session_state:
        st.session_state.qtd_input = 1

    # tab vendas
    with venda:
        df = pd.DataFrame(st.session_state.itens)
        if not df.empty:

            # Remove colunas que não quer mostrar
            df = df.drop(columns=["ean", "preco"], errors="ignore")
            df = df.rename(columns={
                "id_item": "Item",
                "descricao": "Descrição",
                "qtd": "Qtd",
                "total": "Total"})

            # Formata coluna Total como moeda
            df["Total"] = df["Total"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


        col_esq, col_dir = st.columns([1, 3])

        #coluna com a tabela de vendas
        with col_dir:
            item_selecionado = None
            st.markdown(
                f"""
                <div style="text-align: right; font-size: 15px; font-weight: bold; padding-bottom:5px;border-bottom:0px;">
                    Cupom: {id_venda:04d}
                </div>
                """,
                unsafe_allow_html=True)

            if not df.empty:
                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_selection(selection_mode="single", use_checkbox=True)
                gb.configure_default_column(
                    resizable=True,
                    sortable=False,
                    filter=False,
                    editable=False,
                    cellStyle={
                        "fontSize": "16px",
                        "display": "flex",
                        "alignItems": "center"
                    },)

                grid_response = AgGrid(
                    df,
                    gridOptions=gb.build(),
                    height=370,
                    theme="balham",
                    update_mode=GridUpdateMode.SELECTION_CHANGED, # Garante que o Streamlit saiba quando selecionamos algo
                    key="grid_vendas"
                )
                
                # Pegar o item selecionado para exclusão
                item_selecionado = grid_response['selected_rows']
                
            else:
                st.info("Nenhum item adicionado à venda.")
                item_selecionado = None

        # coluna com os inputs de ean e qtd
        with col_esq:      
            try:
                cod = st.text_input("Código EAN", key="ean_input")
                codigo= cod
                        
                col01, col02 = st.columns([2,1])
                with col01:
                    quantid = st.number_input(
                    "Quantidade",
                    min_value=1,
                    step=1,
                    key="qtd_input"
                )
                    qtd = quantid
                    if st.button("➕ Add Item", use_container_width=True):
                        item = criar_item_dto(codigo, qtd, id_venda)
                        
                        if item:
                            st.session_state.itens=item
                            st.rerun()
                        else:
                            st.error("Produto não foi localizado")

                with col02:
                    st.markdown(
                        f"<div style='text-align:left; font-size:14px;padding-bottom:5px; margin-top:0'>Excluir</div>",
                        unsafe_allow_html=True)
                    
                    if st.button("🗑️", use_container_width=True):
                        if item_selecionado is not None:
                            try:

                                if isinstance(item_selecionado, pd.DataFrame) and not item_selecionado.empty:
                                    id_para_excluir = int(item_selecionado['item'].iloc[0])
                                    
                                    item = remover_item(id_para_excluir, id_venda)
                                    if item:
                                        
                                        st.session_state.itens=item 
                                        st.rerun()

                            except Exception as e:
                                st.error(f"Erro ao capturar item: {e}")
                                
                        else:
                            st.info(f"Selecione um item para excluir.")
             
            except ValueError as e:
                st.error(str(e))

            if st.session_state.itens:
                item_atual = st.session_state.itens[-1]
                preco_unit = item_atual["preco"]
                total_item = item_atual["total"]
                desc_item = item_atual["descricao"]
            else:
                preco_unit = total_item = 0.0
                desc_item = "Nova Venda"

            total_venda = sum(i["total"] for i in st.session_state.itens)

            st.markdown(
                f"<div style='text-align:left; font-size:14px;padding-bottom:10px'>Preço Unitario R$</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align:right; font-size:20px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px; background-color: light-silver; padding:10px'> {preco_unit:.2f}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align:left; font-size:14px;padding:10px 0'>Total R$</div>",
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"<div style='text-align:right; font-size:20px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px; background-color: light-silver; padding:10px; margin-bottom:20px'> {total_item:.2f}</div>",
                unsafe_allow_html=True)

        col1 , col2 = st.columns([3,1])
        with col1:
            st.markdown(
            f"<div style='text-align:left; font-size:40px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px;padding:10px'>{desc_item}</div>",
            unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"<div style='text-align:right; font-size:40px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px;  padding:10px;font-weight: bolder'> {total_venda:.2f}</div>",
                unsafe_allow_html=True)


    # tab pesquisa
    with pesquisa:
        st.subheader("Pesquisar")
        pesquisa_descricao = st.text_input("Descrição para busca")
        if pesquisa_descricao:
            dados = buscar_descricao(pesquisa_descricao)

            # if itens:
            #     dados = [{
            #         "EAN": i.ean,
            #         "Descrição": i.descricao,
            #         "Preço": float(i.preco),
            #         "Estoque": i.estoque
            #     } for i in itens]

            df = pd.DataFrame(dados)

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(
                selection_mode="single",
                use_checkbox=True
            )
            gb.configure_grid_options(domLayout="normal")
            grid_options = gb.build()

            grid_response = AgGrid(
                df,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                fit_columns_on_grid_load=True,
                height=205
            )

            if st.button("➕ Adicionar"):
                selecionado = grid_response["selected_rows"]
                if isinstance(selecionado, pd.DataFrame) and not selecionado.empty:
                    codigo = selecionado.iloc[0]["EAN"]
                    item = criar_item_dto(codigo, qtd, id_venda)
                    st.session_state.itens=item
                    st.success("EAN adicionado com sucesso!")
                    time.sleep(2)
                    st.rerun()
                    
                else:
                    st.warning("Selecione um produto primeiro.")
            else:
                st.warning("Nenhum produto encontrado.")
