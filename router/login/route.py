import jwt

from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt.exceptions import InvalidTokenError

from router.login.schemas import (
    LoginRequest,
    TokenResponse,
    UserResponse
)

from core.security import (
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

from router.login.service import authenticate_user


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


security = HTTPBearer(auto_error=False)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):

    user = authenticate_user(
        data.username,
        data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security)
    ]
):

    if credentials is None:
        print("ERROR: No llegó el token")
        raise HTTPException(
            status_code=401,
            detail="No estás autenticado"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("JWT DECODIFICADO:", payload)

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token sin usuario"
            )

    except InvalidTokenError as e:
        print("ERROR JWT:", str(e))

        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    user = authenticate_user_by_token(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    return user


def authenticate_user_by_token(username: str):

    from router.login.service import FAKE_USERS

    return FAKE_USERS.get(username)


@router.get("/me", response_model=UserResponse)
def get_profile(
    current_user: Annotated[dict, Depends(get_current_user)]
):

    return {
        "username": current_user["username"],
        "full_name": current_user["full_name"],
        "role": current_user["role"],
        "permissions": current_user["permissions"]
    }