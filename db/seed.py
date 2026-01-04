from models.db import SessionLocal
from models.user import User
from models.produto import Product

def seed_database():
    db = SessionLocal()

    # 🔐 Criar usuário admin (se não existir)
    admin_exists = db.query(User).filter_by(username="admin").first()
    if not admin_exists:
        admin = User(
            username="admin",
            password="admin123",  # depois podemos criptografar
            is_admin=True
        )
        db.add(admin)

    # 📦 Criar produtos iniciais (se não existirem)
    product_count = db.query(Product).count()

    if product_count == 0:
        produtos = [
            Product(cod="78932321151",name="Arroz 5kg", preco=25.90),
            Product(cod="78932321152",name="Feijão 1kg", preco=8.50),
            Product(cod="78932321153",name="Macarrão", preco=4.20),
            Product(cod="78932321154",name="Óleo de Soja", preco=7.90),
            Product(cod="78932321155",name="Açúcar 1kg", preco=4.80),
            Product(cod="78932321156",name="Café 500g", preco=13.90),
            Product(cod="78932321157",name="Leite 1L", preco=4.50),
            Product(cod="78932321158",name="Farinha de Trigo", preco=5.20),
            Product(cod="78932321159",name="Biscoito", preco=3.80),
            Product(cod="78932321150",name="Refrigerante 2L", preco=9.90),
        ]
        db.add_all(produtos)

    db.commit()
    db.close()
