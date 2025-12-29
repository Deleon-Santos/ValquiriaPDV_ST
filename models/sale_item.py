
from sqlalchemy import Column, Integer, ForeignKey
from .db import Base

class SaleItem(Base):
    __tablename__ = "sale_items"
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)
