import streamlit as st
from PIL import Image
from services.auth_service import login


def render():
    col_img, col_form = st.columns([1, 1])

    
    with col_img:
        img = Image.open("./img/banner_valquiria.png")
        st.image(img, width="stretch")


    with col_form:
        user = st.text_input("Usuário")
        pwd = st.text_input("Senha", type="password")
        st.text(".")
        if st.button("Entrar", width="stretch"):
            usuario = login(user, pwd)

            if usuario:
                st.session_state.logged = True
                st.session_state.usuario_logado = {
                    "id": usuario.id_usuario,
                    "username": usuario.username
                }
                st.rerun()
            else:
                st.error("Login inválido")

    
