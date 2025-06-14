# app/views.py

from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _get_user_or_none(
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
) -> User | None:
    """
    Helper to return the current_user or None (no exception).
    """
    try:
        return get_current_user(session_token=session_token, db=db)
    except HTTPException:
        return None


# Landing page - only greeting
@router.get("/", response_class=HTMLResponse)
def landing_page(
    request: Request,
    user: User | None = Depends(_get_user_or_none),
):
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "user": user,
        },
    )


# Login page (public)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Logout endpoint - clears cookie, redirects home
@router.get("/logout")
def logout_page(session_token: str = Cookie(None)):
    from app.api.deps import sessions

    if session_token and session_token in sessions:
        sessions.pop(session_token)

    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_token")
    return response


# Signup page (public)
@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# Invite page (protected)
@router.get("/invite", response_class=HTMLResponse)
def invite_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "invite.html",
        {
            "request": request,
            "user": current_user,
        },
    )


# Invitation validation page (public)
@router.get("/invitation/validate", response_class=HTMLResponse)
def invitation_validate_page(request: Request):
    return templates.TemplateResponse(
        "invitation_validate.html",
        {"request": request},
    )


# **New** Profile page (protected)
@router.get("/profile", response_class=HTMLResponse)
def profile_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
        },
    )
