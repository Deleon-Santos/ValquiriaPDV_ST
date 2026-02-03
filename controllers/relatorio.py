from datetime import datetime, time
from db.db import SessionLocal
from models.models import Produto, Venda, Item_Venda


def buscar_vendas_por_data(data_inicio, data_fim):
    session =SessionLocal()
    try:
        inicio_dia = datetime.combine(data_inicio, time.min)   
        fim_dia    = datetime.combine(data_fim, time.max)   
        return (
            session.query(Venda)
            .filter(Venda.data_venda.between(inicio_dia, fim_dia))
            .all()
        )
    finally:
        session.close()


def buscar_itens_venda(id_venda):
    with SessionLocal() as session:
        return (
            session.query(Item_Venda, Produto, Venda)
            .join(Produto, Produto.id_produto == Item_Venda.id_produto)
            .join(Venda, Venda.id_venda == Item_Venda.id_venda)
            .filter(Item_Venda.id_venda == id_venda)
            .all()
        )
 