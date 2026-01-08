
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from db.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Produto(Base):
    __tablename__ = "produto"

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    ean = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)

    itens_venda = relationship("Item_Venda", back_populates="produto")

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nome = Column(String, nullable=False, default="USER")
    is_admin = Column(Boolean, default=False)


class Venda(Base):
    __tablename__ = "venda"

    id_venda = Column(Integer, primary_key=True, autoincrement=True)
    total_venda = Column(Float, nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    
    itens = relationship("Item_Venda", back_populates="venda",cascade="all, delete-orphan")


class Item_Venda(Base):
    __tablename__ = "item_venda"

    id_item_venda = Column(Integer, primary_key=True, autoincrement=True)
    id_venda = Column(Integer, ForeignKey("venda.id_venda"), nullable=False)
    id_produto = Column(Integer, ForeignKey("produto.id_produto"), nullable=False)
    qtd = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_venda")