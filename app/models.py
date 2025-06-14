from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    credits = Column(Integer, default=0)  # ← inviter credits
    two_factor_secret = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    invitations_sent = relationship("Invitation", back_populates="inviter")


class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    invited_email = Column(String, index=True)
    inviter_id = Column(Integer, ForeignKey("users.id"))
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    inviter = relationship("User", back_populates="invitations_sent")
