# services/auth_service.py
from db.db import SessionLocal
from models.models import Usuario

def authenticate(user, pwd):
    db = SessionLocal()
    try:
        return db.query(Usuario).filter_by(
            username=user,
            password=pwd
        ).first()
    finally:
        db.close()
