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

        st.markdown(
                f"""
                <div style="text-align: right; font-size: 15px; font-weight: bold; padding-bottom:5px;border-bottom:0px;">
                    Cupom: {id_venda:04d}
                </div>
                """,
                unsafe_allow_html=True)
        st.markdown("""
            <hr style="
                margin: 10px 0;
                border: none;
                height: 1px;
                background: linear-gradient(to right, transparent, #7a7a7a, transparent);
            ">
            """, unsafe_allow_html=True)

        col_esq, col_dir = st.columns([1, 3])

        #coluna com a tabela de vendas
        with col_dir:
            item_selecionado = None
            
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
                    height=355,
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

                # formulario de adição
                with st.form("form_add_item", clear_on_submit=True):

                    cod = st.text_input(
                        "EAN",
                        key="ean_input",
                        placeholder="789012345678",
                    )

                    col01, col02 = st.columns([1,1])

                    with col01:
                        qtd = st.number_input(
                            "Qtd",
                            min_value=1,
                            step=1,
                            key="qtd_input"
                        )

                    with col02:
                        
                        st.markdown("<br>", unsafe_allow_html=True)  # alinhamento
                        submitted = st.form_submit_button("➕", use_container_width=True)

                if submitted:

                    if not cod.strip():
                        st.warning("Digite ou leia um código EAN.")
                        st.stop()

                    item = criar_item_dto(cod, qtd, id_venda)

                    if item:
                        st.session_state.itens = item
                        st.rerun()
                    else:
                        st.error("Produto não foi localizado")
                
                botao_excluir,vazio = st.columns([1,2])
                with botao_excluir:
                    if st.button("🗑️", use_container_width=True):

                        if item_selecionado is None:
                            st.info("Selecione um item para excluir.")
                            st.stop()

                        try:
                            selecionado = item_selecionado

                            if isinstance(selecionado, pd.DataFrame):
                                if selecionado.empty:
                                    st.warning("Selecione um item.")
                                    st.stop()

                                id_para_excluir = int(selecionado.iloc[0]["Item"])

                            else:  # lista
                                id_para_excluir = int(selecionado[0]["Item"])

                            item = remover_item(id_para_excluir, id_venda)

                            if item:
                                st.session_state.itens = item
                                st.rerun()
                            else:
                                st.error("Erro ao remover item.")

                        except Exception as e:
                            st.error(f"Erro ao capturar item: {e}")
                            print(e)
                with vazio:
                    st.markdown("<br>", unsafe_allow_html=True)  # alinhamento
                    

            except ValueError as e:
                st.error(str(e))

            # resumo da venda
            preco_uni, preco_comb = st.columns([1,1])
            if st.session_state.itens:
                item_atual = st.session_state.itens[-1]
                preco_unit = item_atual["preco"]
                total_item = item_atual["total"]
                desc_item = item_atual["descricao"]
            else:
                preco_unit = total_item = 0.0
                desc_item = "Nova Venda"

            total_venda = sum(i["total"] for i in st.session_state.itens)
            with preco_uni:
                st.markdown(
                    f"<div style='text-align:left; font-size:14px; padding:10px 0'>P.Unit R$</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<div style='text-align:right; font-size:25px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px; background-color: light-silver; padding:5px'> {preco_unit:.2f}</div>",
                    unsafe_allow_html=True
                )
            with preco_comb:
                st.markdown(
                    f"<div style='text-align:left; font-size:14px; padding:10px 0'>Total R$</div>",
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"<div style='text-align:right; font-size:25px;border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius: 10px; background-color: light-silver; padding:5px; margin-bottom:5px'> {total_item:.2f}</div>",
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

        with st.form("form_pesquisa", clear_on_submit=True):

            pesquisa_descricao = st.text_input("Descrição para busca")

            submitted = st.form_submit_button("🔍 Buscar")

        # salva resultado
        if submitted:
            st.session_state.resultado_pesquisa = buscar_descricao(pesquisa_descricao) or []

        dados = st.session_state.get("resultado_pesquisa", [])

        if dados:
            df = pd.DataFrame(
                dados,
                columns=["EAN", "Descrição", "Preço", "Estoque"]
            )

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(
                selection_mode="single",
                use_checkbox=True
            )

            grid_response = AgGrid(
                df,
                gridOptions=gb.build(),
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                fit_columns_on_grid_load=True,
                height=200
            )

            #adiciona item atraves da pesquisa por descrição
            quanty = st.number_input(
                "Qtd",      
                min_value=1,
                step=1,     
                value=1,
                key="qtd_pesquisa_input"
            )

            if st.button("➕ Adicionar"):
                item_selecionado = grid_response["selected_rows"]

                if item_selecionado is not None and not item_selecionado.empty:

                    if isinstance(item_selecionado, pd.DataFrame) and not item_selecionado.empty:
                        codigo = item_selecionado['EAN'].iloc[0]

                        item = criar_item_dto(codigo, quanty, id_venda)
                        st.session_state.itens = item

                        st.success("EAN adicionado com sucesso!")
                        time.sleep(1)
                        st.session_state.resultado_pesquisa = []
                        st.rerun()

                else:
                    st.warning("Selecione um produto primeiro.")

        elif submitted:
            st.warning("Nenhum produto encontrado.")
