
import streamlit as st
from models.db import init_db

st.set_page_config(page_title="Valquíria PDV", layout="wide")
init_db()

if "logged" not in st.session_state:
    st.session_state.logged = False
if "cart" not in st.session_state:
    st.session_state.cart = []

if not st.session_state.logged:
    from pages.login import render
    render()
else:
    st.sidebar.title("Valquíria PDV")
    page = st.sidebar.radio("Menu", ["Home","Produtos","Vendas","Relatórios","Sair"])
    if page == "Home":
        from pages.home import render; render()
    elif page == "Produtos":
        from pages.products import render; render()
    elif page == "Vendas":
        from pages.sales import render; render()
    elif page == "Relatórios":
        from pages.reports import render; render()
    elif page == "Sair":
        st.session_state.logged = False
        st.experimental_rerun()
