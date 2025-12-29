
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .db import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
