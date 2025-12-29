
import streamlit as st
from services.auth_service import authenticate

def render():
    st.title("Login")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if authenticate(user,pwd):
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Login inválido")
