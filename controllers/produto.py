from db.db import SessionLocal
from models.models import Produto


def criar_produto(ean: str, descricao: str, preco: float, estoque: int):
    session = SessionLocal()

    # verifica EAN duplicado
    existe = session.query(Produto).filter_by(ean=ean).first()
    if existe:
        session.close()
        raise ValueError("Produto já cadastrado com este EAN")

    produto = Produto(
        ean=ean,
        descricao=descricao,
        preco=preco,
        estoque=estoque
    )

    session.add(produto)
    session.commit()
    session.close()
    return True


def listar_produtos():
    session = SessionLocal()
    produtos = session.query(Produto).all()
    session.close()
    return produtos


def buscar_produto_por_descricao(descricao: str):
    session = SessionLocal()
    try:
        return (
            session.query(Produto)
            .filter(Produto.descricao.ilike(f"%{descricao}%"))
            .all()
        )
    finally:
        session.close()


def buscar_desc(descricao: str):
    session= SessionLocal()
    try:
        return (
            session.query(Produto)
            .filter(Produto.descricao.ilike(f"%{descricao}%"))
            .all()
        )
    finally:
        session.close()