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
    Return the current_user or None (no exception) for public pages.
    """
    try:
        return get_current_user(session_token=session_token, db=db)
    except HTTPException:
        return None


# Landing page – redirect to /invite if already logged in
@router.get("/", response_class=HTMLResponse)
def landing_page(
    request: Request,
    user: User | None = Depends(_get_user_or_none),
):
    if user:
        return RedirectResponse(url="/invite", status_code=302)
    return templates.TemplateResponse(
        "landing.html",
        {"request": request, "user": user},
    )


# Login page – likewise redirect away if already logged in
@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    user: User | None = Depends(_get_user_or_none),
):
    if user:
        return RedirectResponse(url="/invite", status_code=302)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user": user},
    )


# Sign-up page – same redirect logic
@router.get("/signup", response_class=HTMLResponse)
def signup_page(
    request: Request,
    user: User | None = Depends(_get_user_or_none),
):
    if user:
        return RedirectResponse(url="/invite", status_code=302)
    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "user": user},
    )


# Invite page (protected) – user guaranteed by get_current_user
@router.get("/invite", response_class=HTMLResponse)
def invite_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "invite.html",
        {"request": request, "user": current_user},
    )


# Invitation validation page (public) – but still passes user if logged in
@router.get("/invitation/validate", response_class=HTMLResponse)
def invitation_validate_page(
    request: Request,
    user: User | None = Depends(_get_user_or_none),
):
    return templates.TemplateResponse(
        "invitation_validate.html",
        {"request": request, "user": user},
    )


# Profile page (protected)
@router.get("/profile", response_class=HTMLResponse)
def profile_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": current_user},
    )


# Logout endpoint – clears cookie and redirects to landing (which will now go /invite if still logged)
@router.get("/logout")
def logout_page(
    session_token: str = Cookie(None),
):
    from app.api.deps import sessions

    if session_token and session_token in sessions:
        sessions.pop(session_token)

    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_token")
    return response
