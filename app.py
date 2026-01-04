
import streamlit as st
from models.db import init_db
#from pages.vendas import render






st.set_page_config(page_title="Valquíria PDV", layout="wide")
init_db()

if "logged" not in st.session_state:
    st.session_state.logged = False
if "cart" not in st.session_state:
    st.session_state.cart = []

if not st.session_state.logged:
    from pages.login import render; render()
else:
    st.sidebar.title("Valquíria PDV")
    page = st.sidebar.radio("Menu", ["Home","Produtos","Vendas","Relatórios","Sair"])
    if page == "Home":
        from pages.home import render; render()
    elif page == "Produtos":
        from pages.add_produtos import render; render()
    elif page == "Vendas":
        from pages.vendas import render; 
        render()
    elif page == "Relatórios":
        from pages.relatorios import render; render()
    elif page == "Sair":
        st.session_state.logged = False
        st.rerun()
