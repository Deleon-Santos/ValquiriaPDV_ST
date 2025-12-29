from models.db import SessionLocal
from models.sale import Sale

def listar_vendas():
    db = SessionLocal()
    vendas = db.query(Sale).all()
    db.close()
    return vendas
