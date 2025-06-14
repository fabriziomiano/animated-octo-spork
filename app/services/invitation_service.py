import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Invitation, User
from app.email_utils import send_email


async def create_invitation(inviter_id: int, invitee_email: str, db: Session) -> str:
    # 1. Prevent inviting a registered user
    if db.query(User).filter(User.email == invitee_email).first():
        raise ValueError("Cannot invite an already registered user.")

    # 2. Deactivate any existing active invites for this inviter + email
    db.query(Invitation).filter(
        Invitation.inviter_id == inviter_id,
        Invitation.invited_email == invitee_email,
        Invitation.used == False,
    ).update({Invitation.used: True}, synchronize_session=False)
    db.commit()

    # 3. Generate & store the new code
    code = uuid.uuid4().hex
    invitation = Invitation(
        code=code,
        invited_email=invitee_email,
        inviter_id=inviter_id,
        used=False,
        created_at=datetime.utcnow(),
        invited_user_id=None,
    )
    db.add(invitation)
    db.commit()

    # 4. Send invitation email
    link = f"http://localhost:8000/invitation/validate?code={code}"
    body = (
        f"Hello! You have been invited to join CrediMate by user {inviter_id}.\n"
        f"Validate your invite and sign up here:\n{link}"
    )
    await send_email("You’re invited to join CrediMate!", invitee_email, body)
    return code


async def accept_invitation(code: str, new_user_id: int, db: Session):
    """
    Mark invitation used, record who accepted it, and give inviter 1 credit.
    Raises ValueError if:
    - code is invalid or already used
    - the new user's email doesn't match the invitation
    """
    inv = db.query(Invitation).filter(Invitation.code == code).first()
    if not inv:
        raise ValueError("Invalid invitation code.")
    if inv.used:
        raise ValueError("Invitation already used.")

    # Fetch the new user and validate email
    new_user = db.query(User).filter(User.id == new_user_id).first()
    if new_user.email.lower() != inv.invited_email.lower():
        raise ValueError("Invitation code does not match this signup email.")

    # Mark used and record acceptance
    inv.used = True
    inv.invited_user_id = new_user_id

    # Award credit to inviter
    inviter = db.query(User).filter(User.id == inv.inviter_id).first()
    inviter.credits += 1
    db.commit()

    # Notify inviter by email
    body = (
        f"Greetings! Your invitation code {code} was used by {new_user.email}.\n"
        f"You have earned 1 credit. Total credits: {inviter.credits}."
    )
    await send_email("Your invitation was accepted!", inviter.email, body)

    return inviter.id
