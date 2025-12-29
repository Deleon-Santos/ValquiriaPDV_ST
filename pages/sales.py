
import streamlit as st
from services.sale_service import register_sale
from utils.pdf_generator import generate_pdf

def render():
    st.title("Vendas")
    if st.button("Finalizar Venda"):
        sale_id,total = register_sale(st.session_state.cart)
        generate_pdf(sale_id,total)
        st.success(f"Venda {sale_id} finalizada")
        st.session_state.cart = []
