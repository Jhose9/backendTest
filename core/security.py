import os
import jwt

from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash



SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CLAVE-SOLO-PARA-DESARROLLO"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10

password_hash = PasswordHash.recommended()


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_password(plain_password, hashed_password):

    return password_hash.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(password):

    return password_hash.hash(password)


