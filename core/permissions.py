import jwt

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from core.security import SECRET_KEY, ALGORITHM


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security)
    ]
) -> dict:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No estás autenticado"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sin usuario"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    # Import diferido para evitar ciclos con service
    from router.login.service import FAKE_USERS
    user = FAKE_USERS.get(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user


def require_permission(permission: str):
    """
    Factory de dependencia: devuelve una función que valida
    que el usuario autenticado tenga el permiso indicado.
    """

    def permission_checker(
        current_user: dict = Depends(get_current_user)
    ):
        user_permissions = current_user.get("permissions", [])

        # Admin comodín: "*" da acceso a todo
        if "*" in user_permissions:
            return current_user

        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )

        return current_user

    return permission_checker