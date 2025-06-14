# app/api/invite.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models import User
from app.services.invitation_service import create_invitation

router = APIRouter()


class InviteRequest(BaseModel):
    email: EmailStr


@router.post("/invite")
async def invite_user(
    req: InviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Expects JSON: { "email": "invitee@example.com" }
    Only authenticated users may call this.
    """
    try:
        code = await create_invitation(current_user.id, req.email, db)
    except ValueError as e:
        # Already invited
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Invitation sent", "code": code}
