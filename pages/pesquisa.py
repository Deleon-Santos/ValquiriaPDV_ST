import streamlit as st
from controllers.produto import buscar_produto_por_descricao

def render():
    # if not st.session_state.get("abrir_modal"):
    #     return

    # fundo escurecido (efeito modal)
    st.markdown(
        """
        <style>
        .modal-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0,0,0,0.4);
            z-index: 999;
        }
        .modal-box {
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 20px;
            width: 400px;
            border-radius: 10px;
            z-index: 1000;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
        }
        </style>
        <div class="modal-bg"></div>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="modal-box">', unsafe_allow_html=True)

        st.subheader("Buscar produto")

        desc = st.text_input("Descrição", key="busca_desc")

        if st.button("Buscar"):
            st.session_state.resultados = buscar_produto_por_descricao(desc)

        if "resultados" in st.session_state:
            for p in st.session_state.resultados:
                if st.button(f"{p.descricao} | EAN: {p.ean}", key=f"sel_{p.ean}"):
                    st.session_state.ean_input = p.ean
                    st.session_state.abrir_modal = False
                    del st.session_state.resultados
                    st.rerun()

        if st.button("Fechar"):
            st.session_state.abrir_modal = False

        st.markdown("</div>", unsafe_allow_html=True)
