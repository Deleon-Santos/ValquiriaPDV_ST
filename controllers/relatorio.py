from datetime import datetime, time
from db.db import SessionLocal
from models.models import Produto, Venda, Item_Venda

def buscar_vendas_por_data(data):
    session =SessionLocal()
    try:
        inicio_dia = datetime.combine(data, time.min)   # 2026-01-12 00:00:00
        fim_dia    = datetime.combine(data, time.max)   # 2026-01-12 23:59:59.999999

        return (
            session.query(Venda)
            .filter(Venda.data_venda.between(inicio_dia, fim_dia))
            .all()
        )
    finally:
        session.close()


def buscar_itens_venda(id_venda):
    session = SessionLocal()
    try:
        return (
            session.query(Item_Venda, Produto, Venda)
            .join(Produto, Produto.id_produto == Item_Venda.id_produto)
            .join(Venda, Venda.id_venda == Item_Venda.id_venda)
            .filter(Item_Venda.id_venda == id_venda)
            .all()
        )
    finally:
        session.close()
