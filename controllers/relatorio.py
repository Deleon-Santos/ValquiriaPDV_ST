from db.db import SessionLocal
from models.models import Venda

def listar_vendas():
    db = SessionLocal()
    vendas = db.query(Venda).all()
    db.close()
    return vendas
