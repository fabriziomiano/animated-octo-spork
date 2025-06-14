# app/seed.py
from app.models import User
from app.db import Base, engine, SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_db():
    # create tables (idempotent)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(User).filter_by(email="admin@example.com").first():
            user = User(
                name="Admin",
                email="admin@example.com",
                hashed_password=pwd_context.hash("admin123"),
                credits=100,
            )
            db.add(user)
            db.commit()
            print("Seed user created.")
        else:
            print("Seed user already exists.")
    finally:
        db.close()
