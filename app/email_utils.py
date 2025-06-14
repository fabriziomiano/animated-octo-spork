# ------------------ app/email_utils.py ------------------
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Build connection config
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False") == "True",
    USE_CREDENTIALS=True,
)

# FastMail instance
fm = FastMail(conf)


async def send_email(subject: str, email: str, body: str):
    """
    Send an email asynchronously via configured SMTP.
    """
    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype="plain"
    )
    await fm.send_message(message)
