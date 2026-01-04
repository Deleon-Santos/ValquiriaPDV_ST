
import streamlit as st
from models.db import SessionLocal
from models.venda import Venda

def render():
    st.title("Relatórios")
    db = SessionLocal()
    for s in db.query(Venda).all():
        st.write(s.id, s.total, s.created_at)
    db.close()
