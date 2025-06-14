import uuid
import datetime as dt
from sqlalchemy.orm import Session
from app.models import Invitation, User
from app.email_utils import send_email

# Invitations expire after 48 hours
INVITE_EXPIRE_HOURS = 48


async def create_invitation(inviter_id: int, invite_email: str, db: Session) -> str:
    """
    Create an invitation and send the email.
    Raises ValueError if an unused invite already exists.
    Returns the code.
    """
    existing = (
        db.query(Invitation)
        .filter(Invitation.invited_email == invite_email, Invitation.used == False)
        .first()
    )
    if existing:
        raise ValueError("User already invited")

    code = uuid.uuid4().hex
    # inv = Invitation(code=code, invited_email=invite_email, inviter_id=inviter_id)
    # db.add(inv)
    # db.commit()

    link = f"http://localhost:8000/signup?invite={code}"
    subject = "You're invited to MyApp!"
    body = f"Hi,\n\nPlease join MyApp using this link (expires in {INVITE_EXPIRE_HOURS} hours):\n\n{link}"

    await send_email(subject=subject, recipients=[invite_email], body=body)
    return code


def validate_invitation_code(code: str, db: Session) -> bool:
    """
    Returns True if the code exists, is unused, and not expired.
    """
    inv = db.query(Invitation).filter(Invitation.code == code).first()
    if not inv or inv.used:
        return False
    if dt.now(dt.datetime.timezone.utc) > inv.created_at + dt.timedelta(
        hours=INVITE_EXPIRE_HOURS
    ):
        return False
    return True


def mark_invitation_used(code: str, db: Session, credit_amount: int = 10):
    """
    Mark the invitation as used and credit the inviter.
    """
    inv = db.query(Invitation).filter(Invitation.code == code).first()
    if not inv or inv.used:
        raise ValueError("Invalid or already used invitation code")

    # Check expiration
    if dt.now(dt.datetime.timezone.utc) > inv.created_at + dt.timedelta(
        hours=INVITE_EXPIRE_HOURS
    ):
        raise ValueError("Invitation code has expired")

    inv.used = True
    inviter = db.query(User).get(inv.inviter_id)
    inviter.credits += credit_amount
    db.commit()
