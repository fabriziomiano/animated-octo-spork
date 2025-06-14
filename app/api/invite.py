# app/api/invite.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models import Invitation, User
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
    Create a new invitation code for the given email.
    """
    try:
        code = await create_invitation(
            current_user.id, current_user.name, req.email, db
        )
    except ValueError as e:
        # e.g. "already invited" or "already registered"
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Invitation sent", "code": code}


@router.get("/invitation/validate")
def validate_invitation(
    code: str,
    db: Session = Depends(get_db),
):
    """
    Check whether an invitation code exists and is still unused.
    Returns {"valid": true} or {"valid": false}.
    """
    inv = db.query(Invitation).filter(Invitation.code == code).first()
    return {"valid": bool(inv and not inv.used)}
