
# pages/login.py
import streamlit as st
from services.auth_service import authenticate

def render():
    st.markdown("""
    <style>
    /* Estilo geral dos inputs */
    input[type="text"], input[type="password"] {
        color: black;
        background-color: #FFFFFF;
        border-bottom: 3px solid silver;
        border-right: 3px solid silver;
        border-radius: 10px;
        
        padding: 10px;
    }

    
    
    </style>
    """, unsafe_allow_html=True)
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
