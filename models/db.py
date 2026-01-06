
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///db/valquiria.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
    from models.user import User
    from models.produto import Product
    from models.venda import Venda
    from models.item import Venda_Item

    Base.metadata.create_all(bind=engine)

    # 🌱 Seed inicial
    from db.seed import seed_database
    seed_database()
