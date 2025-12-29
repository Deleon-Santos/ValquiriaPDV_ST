from services.auth_service import authenticate

def login(username: str, password: str) -> bool:
    if not username or not password:
        return False
    return authenticate(username, password)
