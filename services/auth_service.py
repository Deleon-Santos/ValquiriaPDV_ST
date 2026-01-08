
from db.db import SessionLocal
from models.user import User

def authenticate(user, pwd):
    db = SessionLocal()
    u = db.query(User).filter_by(username=user, password=pwd).first()
    db.close()
    return u
