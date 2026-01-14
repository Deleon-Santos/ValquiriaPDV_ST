
import streamlit as st
from db.db import SessionLocal
from models.models import Venda

def render():
    st.title("Relatórios")
    db = SessionLocal()
    for s in db.query(Venda).all():
        st.write(s.id_venda, s.total, s.created_at)
    db.close()
