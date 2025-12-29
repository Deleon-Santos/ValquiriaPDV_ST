
from models.db import SessionLocal
from models.product import Product

def create_product(name, price, stock):
    db = SessionLocal()
    p = Product(name=name, price=price, stock=stock)
    db.add(p)
    db.commit()
    db.close()

def list_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products
