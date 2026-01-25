import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = st.secrets.get("DATABASE_URL") 
if not DATABASE_URL:

    st.error("DATABASE_URL não configurada!")
    st.stop()

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# engine = create_engine("sqlite:///db/valquiria.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db():
   
    from models.models import Produto, Usuario, Venda, Item_Venda
    

    Base.metadata.create_all(bind=engine)

    from db.seed import seed_database
    seed_database()
