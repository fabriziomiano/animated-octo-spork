# app/email_utils.py

import os
from dotenv import load_dotenv
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr, ValidationError, parse_obj_as

# Load environment variables from .env
load_dotenv()

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

print(conf.MAIL_USERNAME)
print(os.getenv("MAIL_PASSWORD"))
print(conf.MAIL_FROM)
print(conf.MAIL_PORT)
print(conf.MAIL_SERVER)
print(conf.MAIL_STARTTLS)
print(conf.MAIL_SSL_TLS)

fm = FastMail(conf)


async def send_email(subject: str, recipients: List[str], body: str):
    """
    Send an email.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="plain",
    )
    await fm.send_message(message)
