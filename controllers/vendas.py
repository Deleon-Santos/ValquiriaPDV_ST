import datetime
from sqlalchemy import func
from db.db import SessionLocal
from models.models import Item_Venda, Produto, Usuario, Venda
from datetime import datetime
from sqlalchemy import func


def iniciar_venda(usuario: dict) -> int:
    
    with SessionLocal() as session: 
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

            return nova_venda.id_venda

        except Exception as e:
            session.rollback()
            raise e


def criar_item(cod: str, qtd: int, id_venda: int) -> Item_Venda | None: 
    with SessionLocal() as session:

        try:# valida produto NA MESMA SESSÃO
            produto = session.query(Produto).filter(Produto.ean == cod).first()

            if not produto:
                return None          

            # determina o próximo número de item
            ultimo_item = (
                session.query(func.max(Item_Venda.n_item))
                .filter(Item_Venda.id_venda == id_venda)
                .scalar()
            )
            proximo_item = 1 if ultimo_item is None else ultimo_item + 1

            # cria o item da venda
            novo_item = Item_Venda(
                n_item = proximo_item,
                id_venda = id_venda,
                id_produto =produto.id_produto,
                qtd=qtd,
                total=float(produto.preco * qtd)
            )
            session.add(novo_item)
            session.commit()

            # atualiza o total da venda
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
            
            # retorna o item criado em formato de lista de dicionários  
            return carrinho_atual(id_venda)

        except Exception as e:
            session.rollback()
            return None

    
def delete_item(n_item, id_venda):
    with SessionLocal() as session:
        try:
            delete_item = session.query(Item_Venda).filter(
                Item_Venda.n_item == n_item,
                Item_Venda.id_venda == id_venda
            )

            # Verifica se o item existe antes de tentar deletar
            if delete_item.first():
                delete_item.delete(synchronize_session=False)
                session.commit()
                
                total_venda = (
                    session.query(func.sum(Item_Venda.total))
                    .filter(Item_Venda.id_venda == id_venda)
                    .scalar()
                ) or 0.0

                venda = session.query(Venda).get(id_venda)
                venda.total_venda = total_venda       

                session.commit()
                return True
            
            return False

        except Exception as e:
            session.rollback() # Reverte se houver erro de rede ou banco
            return False
        

def carrinho_atual(id_venda):
    with SessionLocal() as session:
        itens = (
                    session.query(Item_Venda)
                    .join(Produto)
                    .filter(Item_Venda.id_venda == id_venda)
                    .all()
                    )

        return [
            {
            "id_item": item.n_item,
            "ean": item.produto.ean,
            "descricao": item.produto.descricao,
            "qtd": item.qtd,
            "preco": item.produto.preco,
            "total": item.total
        }
        for item in itens
        ]
