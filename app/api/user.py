from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
