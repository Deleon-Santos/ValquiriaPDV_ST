import streamlit as st
from services.pagamento_service import (obter_venda_aberta,processar_pagamento)

def render():
    st.title("Pagamento")

    usuario = st.session_state.usuario_logado
    if not usuario:
        st.error("Usuário não autenticado")
        return

    venda = obter_venda_aberta(usuario)

    if not venda:
        st.warning("Nenhuma venda aberta para este usuário")
        return

    st.metric("Total da Venda", f"R$ {venda.total_venda:.2f}")

    forma_pagamento = st.radio(
        "Forma de Pagamento",
        ["Dinheiro", "PIX", "Cartão"]
    )

    valor_pago = st.number_input(
        "Valor Pago",
        min_value=0.0,
        step=0.50,
        format="%.2f"
    )

    if st.button("Finalizar Pagamento"):
        resultado = processar_pagamento(
            id_venda=venda.id_venda,
            total_venda=venda.total_venda,
            forma_pagamento=forma_pagamento.lower(),
            valor_pago=valor_pago
        )

        if resultado["status"] == "erro":
            st.error(resultado["mensagem"])
        else:
            st.success("Pagamento efetuado com sucesso!")

            if resultado.get("troco", 0) > 0:
                st.info(f"Troco: R$ {resultado['troco']:.2f}")
