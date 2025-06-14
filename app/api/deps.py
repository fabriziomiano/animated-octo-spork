from fastapi import Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import secrets

from app.db import SessionLocal, Base, engine
from app.models import User


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Simple in-memory session store (demo only)
sessions = {}


def create_session(user_id: int):
    token = secrets.token_hex(32)
    sessions[token] = user_id
    return token


def get_current_user(session_token: str = Cookie(None), db: Session = Depends(get_db)):
    if session_token is None or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = sessions[session_token]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
