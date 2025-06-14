# app/views.py

from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Landing page – only greeting
@router.get("/", response_class=HTMLResponse)
def landing_page(
    request: Request,
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
):
    user_name = None
    try:
        user: User = get_current_user(session_token=session_token, db=db)
        user_name = user.name
    except HTTPException:
        pass

    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "user_name": user_name,
        },
    )


# Login page
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout")
def logout_page(session_token: str = Cookie(None)):
    """
    Clear the session cookie and redirect back to the landing page (guest view).
    """
    from app.api.deps import sessions

    if session_token and session_token in sessions:
        sessions.pop(session_token)
    # Build a redirect response to "/"
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_token")
    return response


# Signup page
@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# Invite page (protected, redirects if not logged in)
@router.get("/invite", response_class=HTMLResponse)
def invite_page(
    request: Request,
    session_token: str = Cookie(None),
    db: Session = Depends(get_db),
):
    try:
        current_user: User = get_current_user(session_token=session_token, db=db)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "invite.html",
        {
            "request": request,
            "user_name": current_user.name,
        },
    )


# Invitation validation page
@router.get("/invitation/validate", response_class=HTMLResponse)
def invitation_validate_page(request: Request):
    return templates.TemplateResponse(
        "invitation_validate.html",
        {"request": request},
    )
