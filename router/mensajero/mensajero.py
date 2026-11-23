from fastapi import APIRouter, Depends

from core.permissions import require_permission

router = APIRouter(
    prefix="/mensajero",
    tags=["Mensajero"]
)


@router.get("/")
def get_mensajeros(
    current_user: dict = Depends(
        require_permission("mensajero")
    )
):

    return {
        "message": "Acceso autorizado al módulo Mensajero"
    }