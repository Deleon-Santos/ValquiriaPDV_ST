
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///db/valquiria.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
   
    from models.models import Produto, Usuario, Venda, Item_Venda
    

    Base.metadata.create_all(bind=engine)

    from db.seed import seed_database
    seed_database()
