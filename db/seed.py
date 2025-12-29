from models.db import SessionLocal
from models.user import User
from models.product import Product

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
            Product(name="Arroz 5kg", price=25.90, stock=50),
            Product(name="Feijão 1kg", price=8.50, stock=40),
            Product(name="Macarrão", price=4.20, stock=60),
            Product(name="Óleo de Soja", price=7.90, stock=30),
            Product(name="Açúcar 1kg", price=4.80, stock=45),
            Product(name="Café 500g", price=13.90, stock=25),
            Product(name="Leite 1L", price=4.50, stock=80),
            Product(name="Farinha de Trigo", price=5.20, stock=35),
            Product(name="Biscoito", price=3.80, stock=70),
            Product(name="Refrigerante 2L", price=9.90, stock=20),
        ]
        db.add_all(produtos)

    db.commit()
    db.close()
