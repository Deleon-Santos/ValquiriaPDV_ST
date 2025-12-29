
import streamlit as st
from models.db import SessionLocal
from models.sale import Sale

def render():
    st.title("Relatórios")
    db = SessionLocal()
    for s in db.query(Sale).all():
        st.write(s.id, s.total, s.created_at)
    db.close()
