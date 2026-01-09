
from db.db import SessionLocal
from models.models import Usuario

def authenticate(user, pwd):
    db = SessionLocal()
    u = db.query(Usuario).filter_by(username=user, password=pwd).first()
    db.close()
    return u
