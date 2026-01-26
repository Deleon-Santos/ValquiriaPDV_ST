import streamlit as st
from db.db import init_db
from PIL import Image


st.set_page_config(page_title="Valquíria PDV", layout="wide",page_icon="./img/banner_valquiria.png",)
init_db()

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background-color: lightblue;
        padding: 5px;
    }
    input[type="text"], input[type="number"], input[type="password"] {color:black; background-color:white; border:.5px solid silver;border-bottom:3px solid silver;border-right:3px solid silver; border-radius:10px; font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True)

if "logged" not in st.session_state:
    st.session_state.logged = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if not st.session_state.logged:
    st.session_state.usuario_logado = None
    from pages.login import render; render()

else:
    st.sidebar.title("Valquíria PDV")
    page = st.sidebar.radio("Menu", ["Produtos","Vendas","Pagamento","Relatórios","Sair"])
    
    if page == "Vendas":
        from pages.vendas import render; 
        render()

    elif page == "Produtos":
        from pages.add_produtos import render; 
        render()
    
    elif page == "Pagamento":
        from pages.pagamento import render;
        render()

    elif page == "Relatórios":
        from pages.relatorios import render; 
        render()

    elif page == "Sair":
        st.session_state.logged = False    
        st.session_state.usuario_logado = None
        st.rerun()
