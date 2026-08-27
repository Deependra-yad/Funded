import resend
import random
from fastapi import APIRouter, Depends, Request, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User
from app.security import hash_password, verify_password, create_session_token, get_optional_user, require_auth
from app.config import SESSION_COOKIE_NAME, APP_NAME, APP_TAGLINE
import uuid

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: str = "/dashboard", error: str = None, logged_out: str = None, db: Session = Depends(get_db)):
    user = await get_optional_user(request, db)
    if user:
        return RedirectResponse(url=next or "/dashboard", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "app_name": APP_NAME,
            "next": next,
            "error": error,
            "logged_out": bool(logged_out)
        }
    )

@router.post("/login")
async def handle_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form("/dashboard"),
    remember_me: str = Form(None),
    db: Session = Depends(get_db)
):
    email_clean = email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    
    
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "app_name": APP_NAME,
                "next": next,
                "error": "Invalid email or password."
            }
        )

    if user.deletion_requested:
        return templates.TemplateResponse(
            request=request,
            name="cancel_deletion.html",
            context={
                "app_name": APP_NAME,
                "email": user.email
            }
        )


    # If user has no password set (e.g. from seed migration), set it now
    if not user.hashed_password:
        user.hashed_password = hash_password(password)
        user.plain_password = password
        db.commit()
    el
    if not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"app_name": APP_NAME, "next": next, "error": "Invalid email or password.", "email": email_clean}
        )
        
    if not user.is_email_verified:
        return RedirectResponse(url=f"/verify-email?email={email_clean}", status_code=303)

    token = create_session_token(user.id)

        response = RedirectResponse(url="/dashboard?welcome=1", status_code=303)
        response.set_cookie(key=SESSION_COOKIE_NAME, value=token, httponly=True, max_age=86400 * 30, samesite="lax")
        return response
    else:
        return templates.TemplateResponse(request=request, name="verify.html", context={"app_name": APP_NAME, "email": email, "error": "Invalid verification code."})
