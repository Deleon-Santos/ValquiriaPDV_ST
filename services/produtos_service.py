
from models.db import SessionLocal
from models.produto import Product

def create_product(name, preco, qtd):
    db = SessionLocal()
    p = Product(name=name, preco=preco , qtd=qtd)
    db.add(p)
    db.commit()
    db.close()

def list_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products
