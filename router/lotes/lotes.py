from fastapi import APIRouter, Depends

from core.permissions import require_permission

router = APIRouter(
    prefix="/lotes",
    tags=["Lotes"]
)


@router.get("/")
def get_lotes(
    current_user: dict = Depends(
        require_permission("lotes")
    )
):

    return {
        "message": "Acceso autorizado al módulo Lotes"
    }