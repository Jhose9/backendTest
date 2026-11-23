from core.security import (
    get_password_hash,
    verify_password
)

# Usuarios simulados (sin base de datos)
FAKE_USERS = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador",
        "role": "admin",
        "permissions": ["*"],
        "hashed_password": get_password_hash("Admin123")
    },

    "usuario1": {
        "username": "usuario1",
        "full_name": "Usuario Mensajero",
        "role": "user",
        "permissions": ["mensajero"],
        "hashed_password": get_password_hash("1234")
    },

    "usuario2": {
        "username": "usuario2",
        "full_name": "Usuario Operativo",
        "role": "user",
        "permissions": ["mensajero", "lotes"],
        "hashed_password": get_password_hash("1234")
    },

    "usuario3": {
        "username": "usuario3",
        "full_name": "Usuario Supervisor",
        "role": "user",
        "permissions": ["mensajero", "lotes", "reportes"],
        "hashed_password": get_password_hash("1234")
    }
}

def authenticate_user(username: str, password: str):

    user = FAKE_USERS.get(username)

    if not user:
        return None

    if not verify_password(
        password,
        user["hashed_password"]
    ):
        return None

    return user

def get_user_by_username(username: str):

    return FAKE_USERS.get(username)