
from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    cod = Column(String, unique=True)
    name = Column(String)
    preco = Column(Float)
    
