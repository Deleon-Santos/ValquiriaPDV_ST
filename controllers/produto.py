from db.db import SessionLocal
from models.models import Produto


def criar_produto(ean: str, descricao: str, preco: float, estoque: int):
    with SessionLocal() as session:

        # verifica EAN duplicado
        existe = session.query(Produto).filter_by(ean=ean).first()
        if existe:
            session.close()
            raise ValueError("Produto já cadastrado com este EAN")

        produto = Produto(
            ean=ean,
            descricao=descricao,
            preco=preco,
            estoque=estoque)

        session.add(produto)
        session.commit()
        return True


def listar_produtos():
    with SessionLocal() as session:
        produtos = session.query(Produto).all()
        return produtos


def buscar_produto_por_descricao(pesquisa_descricao: str):
    with SessionLocal() as session:
        return (
            session.query(Produto)
            .filter(Produto.descricao.ilike(f"%{pesquisa_descricao}%"))
            .all())
        

