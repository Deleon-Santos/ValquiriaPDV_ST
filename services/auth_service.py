from services.auth_service import autenticacao

def login(username: str, password: str) -> bool:
    if not username or not password:
        return False
    return autenticacao(username, password)
