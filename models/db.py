
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///db/valquiria.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from models.user import User
    from models.product import Product
    from models.sale import Sale
    from models.sale_item import SaleItem

    Base.metadata.create_all(bind=engine)

    # 🌱 Seed inicial
    from db.seed import seed_database
    seed_database()
