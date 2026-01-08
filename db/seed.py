from db.db import SessionLocal
#from passlib.context import CryptContext
from models.models import Produto, Usuario

def seed_database():
    db = SessionLocal()

   
    admin_exists = db.query(Usuario).filter_by(username="admin").first()
    if not admin_exists:
        admin = Usuario(
            username="admin",
            password="admin123",  # depois podemos criptografar
            
            is_admin=True
        )
        db.add(admin)

    product_count = db.query(Produto).count()

    if product_count == 0:
        produtos = [
            Produto(ean="78932321151",descricao="Arroz 5kg", preco=25.90, estoque = 20),
            Produto(ean="78932321152",descricao="Feijão 1kg", preco=8.50,  estoque = 20),
            Produto(ean="78932321153",descricao="Macarrão", preco=4.20, estoque = 20),
            Produto(ean="78932321154",descricao="Óleo de Soja", preco=7.90, estoque = 20),
            Produto(ean="78932321155",descricao="Açúcar 1kg", preco=4.80, estoque = 20),
            Produto(ean="78932321156",descricao="Café 500g", preco=13.90, estoque = 20),
            Produto(ean="78932321157",descricao="Leite 1L", preco=4.50, estoque = 20),
            Produto(ean="78932321158",descricao="Farinha de Trigo", preco=5.20, estoque = 20),
            Produto(ean="78932321159",descricao="Biscoito", preco=3.80, estoque = 20),
            Produto(ean="78932321150",descricao="Refrigerante 2L", preco=9.90, estoque = 20),
        ]
        db.add_all(produtos)
        admin = Usuario(
            username="admin",
            password="admin123",
            nome="Administrador",
            is_admin=True
        )
        db.add(admin)
        

    db.commit()
    db.close()
