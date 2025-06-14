# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=0)
    two_factor_secret = Column(String, nullable=True)

    # Who invited this user (nullable for organic signups)
    invited_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    invited_by = relationship(
        "User",
        remote_side=[id],
        backref="invitees",
        foreign_keys=[invited_by_id],
    )

    # Invitations *this user has sent*
    invitations_sent = relationship(
        "Invitation",
        foreign_keys="Invitation.inviter_id",
        back_populates="inviter",
        cascade="all, delete-orphan",
    )

    # Invitations *this user has received (and accepted)*
    invitations_received = relationship(
        "Invitation",
        foreign_keys="Invitation.invited_user_id",
        back_populates="invited_user",
        cascade="all, delete-orphan",
    )


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    invited_email = Column(String, nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    used = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Who sent this invite
    inviter = relationship(
        "User",
        foreign_keys=[inviter_id],
        back_populates="invitations_sent",
    )

    # Who accepted (signed up with) this invite
    invited_user = relationship(
        "User",
        foreign_keys=[invited_user_id],
        back_populates="invitations_received",
    )
