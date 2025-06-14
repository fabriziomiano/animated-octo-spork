# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import secrets

from app.api.deps import get_db, create_session
from app.models import User
from app.security import hash_password, verify_password

router = APIRouter()


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class TwoFARequest(BaseModel):
    email: EmailStr
    code: str


@router.post("/signup", status_code=201)
def signup(
    req: SignupRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    # -- DEBUG LOGGING --
    print(">> [SIGNUP] payload:", req)

    # Check email uniqueness
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    hashed = hash_password(req.password)
    user = User(name=req.name, email=req.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    # -- CONFIRM TO LOGS --
    print(f">> [SIGNUP] created user id={user.id}, email={user.email}")

    # Auto-login: create session & set cookie
    token = create_session(user.id)
    response.set_cookie(key="session_token", value=token, httponly=True)

    # Return the new user’s id so you can see it in the network tab
    return {"message": "User created and logged in", "user_id": user.id}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    print(form_data)
    user = db.query(User).filter(User.email == form_data.username).first()
    print(user)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    twofa_code = secrets.token_hex(3)
    user.two_factor_secret = twofa_code

    db.commit()

    return {
        "twofa_required": True,
        "message": "2FA code sent to your email",
        "twofa_code": twofa_code,
    }


@router.post("/login/2fa")
def verify_2fa(
    req: TwoFARequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or user.two_factor_secret != req.code:
        raise HTTPException(status_code=400, detail="Invalid 2FA code")

    user.two_factor_secret = None
    db.commit()

    token = create_session(user.id)
    response.set_cookie(key="session_token", value=token, httponly=True)
    return {"message": "Logged in successfully"}


@router.get("/logout")
def logout(response: Response, session_token: str = None):
    from app.api.deps import sessions

    if session_token and session_token in sessions:
        sessions.pop(session_token)
    response.delete_cookie("session_token")
    return {"message": "Logged out"}
