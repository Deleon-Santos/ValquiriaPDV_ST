import datetime
from sqlalchemy import func
from db.db import SessionLocal
from models.models import Item_Venda, Produto, Usuario, Venda


from datetime import datetime

def iniciar_venda(usuario: dict) -> int:
    if usuario is None:
        raise ValueError("Usuário obrigatório para iniciar venda")
    session = SessionLocal()
    
    try:
        # verifica se já existe venda aberta
        venda_aberta = session.query(Venda).filter(Venda.status == "aberta",Venda.id_usuario == usuario['id']).first()
        
        if venda_aberta:
            return venda_aberta.id_venda

        # cria nova venda
        nova_venda = Venda(
            data_venda=datetime.now(),
            status="aberta",
            total_venda=0.0,
            id_usuario=usuario['id']
        )

        session.add(nova_venda)
        session.commit()

        # garante que o ID foi gerado
        session.refresh(nova_venda)

        print(f"Comanda #{nova_venda.id_venda} criada.")
        return nova_venda.id_venda

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def criar_item(cod: str, qtd: int,usuario:dict ) -> Item_Venda | None:
    id_venda = iniciar_venda(usuario)
    print(id_venda)
    session = SessionLocal()
    

    try:
        # valida produto NA MESMA SESSÃO
        produto = session.query(Produto).filter(Produto.ean == cod).first()
        print(f"produto dentro de criar aitem {produto.descricao}")

        if not produto:
            return None

        novo_item = Item_Venda(
            id_venda = id_venda,
            id_produto =produto.id_produto,
            qtd=qtd,
            total=float(produto.preco * qtd)
        )

        session.add(novo_item)
        session.commit()


        total_venda = (
            session.query(func.sum(Item_Venda.total))
            .filter(Item_Venda.id_venda == id_venda)
            .scalar()
        ) or 0.0

        venda = session.query(Venda).get(id_venda)
        venda.total_venda = total_venda       

        session.commit()
        
        # garante que o objeto está sincronizado
        session.refresh(novo_item)

        return novo_item

    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar produto: {e}")
        return None

    finally:
        session.close()

    
