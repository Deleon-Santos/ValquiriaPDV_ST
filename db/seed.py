from db.db import SessionLocal
#from passlib.context import CryptContext
from models.models import Produto, Usuario

def seed_database():
    db = SessionLocal()

    product_count = db.query(Produto).count()
    if product_count == 0:
        produtos = [
            Produto(ean="78932321151",descricao="Arroz polido Solito 5kg", preco=25.90, estoque = 20),
            Produto(ean="78932321152",descricao="Feijão Carioca Kicaldo 1kg", preco=8.50,  estoque = 20),
            Produto(ean="78932321153",descricao="Macarrão Adria Spagette 500g", preco=4.20, estoque = 20),
            Produto(ean="78932321154",descricao="Óleo de Soja Liza 900ml", preco=7.90, estoque = 20),
            Produto(ean="78932321155",descricao="Açúcar refinado Uniao 1kg", preco=4.80, estoque = 20),
            Produto(ean="78932321156",descricao="Café extra forte Pele 500g", preco=13.90, estoque = 20),
            Produto(ean="78932321157",descricao="Leite UHT ninho integral 1L", preco=4.50, estoque = 20),
            Produto(ean="78932321158",descricao="Farinha de TrigoDona Benta 1kg", preco=5.20, estoque = 20),
            Produto(ean="78932321159",descricao="Biscoito rechedo Negresco 350g", preco=3.80, estoque = 20),
            Produto(ean="78932321150",descricao="Refrigerante Coca-Cola 2L", preco=9.90, estoque = 20),
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
    else:
        db.close()
