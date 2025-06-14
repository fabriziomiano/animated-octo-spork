# app/seed.py
"""
Seed script to initialize the database with a default admin user.
This script checks if an admin user exists, and if not, creates one with a default password.
"""

import os
from app.models import User
from app.db import Base, engine, SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def seed_db():
    # create tables (idempotent)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(User).filter_by(email="admin@example.com").first():
            user = User(
                name=ADMIN_NAME,
                email=ADMIN_EMAIL,
                hashed_password=pwd_context.hash(ADMIN_PASSWORD),
                credits=100,
            )
            db.add(user)
            db.commit()
            print("Seed user created.")
        else:
            print("Seed user already exists.")
    finally:
        db.close()
