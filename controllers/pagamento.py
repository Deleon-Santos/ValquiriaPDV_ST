from db.db import SessionLocal
from models.models import Venda


def buscar_venda_aberta(id_usuario: int):
    with SessionLocal() as session:
        return (
            session.query(Venda)
            .filter(
                Venda.status == "aberta",
                Venda.id_usuario == id_usuario
            )
            .first()
        )
  
def efetuar_pagamento(
    id_venda: int,
    total_venda: float,
    forma_pagamento: str,
    valor_pago: float,
    troco: float
) -> dict:

    with SessionLocal() as session:
        venda = session.query(Venda).filter_by(id_venda=id_venda).first()

        if not venda:
            return {"status": "erro", "mensagem": "Venda não encontrada"}

        if venda.status != "aberta":
            return {"status": "erro", "mensagem": "Venda já finalizada"}
        
        if forma_pagamento in ["pix", "cartão"]:
            valor_pago = total_venda
    
        if forma_pagamento not in ["dinheiro", "pix", "cartão"]:
            return {"status": "erro", "mensagem": "Forma de pagamento inválida"}

        if valor_pago < total_venda:
            return {
                "status": "erro",
                "mensagem": "Valor pago insuficiente"
            }

        troco = 0.0

        if forma_pagamento == "dinheiro":
            troco = round(valor_pago - total_venda, 2)

        # Atualiza o status davenda
        venda.status = "pago"
        venda.total_venda = total_venda
        venda.forma_pagamento = forma_pagamento
        venda.valor_pago = valor_pago
        venda.troco = troco
        session.commit()

        return {
            "status": "ok",
            "troco": troco
        }

   