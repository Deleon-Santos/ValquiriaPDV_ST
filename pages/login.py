
# pages/login.py
import streamlit as st
from services.auth_service import authenticate

def render():
    st.title("Login")

    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = authenticate(user, pwd)

        if usuario:
            st.session_state.logged = True
            st.session_state.usuario_logado = {
                "id": usuario.id_usuario,
                "username": usuario.username
            }
            st.rerun()
        else:
            st.error("Login inválido")
