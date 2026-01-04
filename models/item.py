
from sqlalchemy import Column, Integer, ForeignKey
from .db import Base

class Venda_Item(Base):
    __tablename__ = "venda_items"
    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey("venda.id"))
    produto_id = Column(Integer)
    
