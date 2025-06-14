# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.auth import router as auth_router
from app.api.invite import router as invite_router
from app.api.user import router as user_router
from app.views import router as views_router

from app.db import Base, engine

# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.db import engine, Base
from app.api.auth import router as auth_router
from app.api.invite import router as invite_router
from app.api.user import router as user_router
from app.views import router as views_router
from app.seed import seed_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup logic ---
    # create tables & seed initial data
    seed_db()
    yield
    # --- shutdown logic (if any) ---
    # e.g., close external connections


# pass lifespan to FastAPI
app = FastAPI(lifespan=lifespan)

# static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# include routers
app.include_router(auth_router, prefix="/api")
app.include_router(invite_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(views_router)
