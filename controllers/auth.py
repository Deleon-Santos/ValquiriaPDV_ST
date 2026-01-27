from db.db import SessionLocal
from models.models import Usuario


def autenticacao(user, pwd):
    with SessionLocal() as session:
        return session.query(Usuario).filter_by(
            username=user,
            password=pwd
        ).first()
  