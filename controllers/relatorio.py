from models.db import SessionLocal
from models.venda import Venda

def listar_vendas():
    db = SessionLocal()
    vendas = db.query(Venda).all()
    db.close()
    return vendas
