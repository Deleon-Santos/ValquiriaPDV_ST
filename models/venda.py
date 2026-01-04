
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .db import Base

class Venda(Base):
    __tablename__ = "venda"
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
