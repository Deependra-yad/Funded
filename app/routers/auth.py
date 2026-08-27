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
    elif not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "app_name": APP_NAME,
                "next": next,
                "error": "Incorrect password. Please try again.",
                "email": email_clean
            }
        )

    # Issue session cookie
    
    if remember_me == "true":
        token = create_session_token(user.id, expires_in_seconds=86400 * 30) # 30 days
        max_age = 86400 * 30
    else:
        token = create_session_token(user.id, expires_in_seconds=86400 * 7) # 7 days
        max_age = None # Session cookie (expires when browser closes)

    target_url = next if next and not next.startswith("/login") else "/dashboard"
    response = RedirectResponse(url=target_url, status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=max_age,
        expires=max_age,
        samesite="lax"
    )
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, next: str = "/dashboard", error: str = None, db: Session = Depends(get_db)):
    user = await get_optional_user(request, db)
    if user:
        return RedirectResponse(url=next or "/dashboard", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "app_name": APP_NAME,
            "next": next,
            "error": error
        }
    )

@router.post("/register")
async def handle_register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    next: str = Form("/dashboard"),
    remember_me: str = Form(None),
    db: Session = Depends(get_db)
):
    email_clean = email.strip().lower()
    name_clean = full_name.strip()

    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "app_name": APP_NAME,
                "next": next,
                "error": "Password must be at least 6 characters.",
                "full_name": name_clean,
                "email": email_clean
            }
        )

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "app_name": APP_NAME,
                "next": next,
                "error": "Passwords do not match.",
                "full_name": name_clean,
                "email": email_clean
            }
        )

    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "app_name": APP_NAME,
                "next": next,
                "error": "An account with this email already exists. Please log in.",
                "email": email_clean
            }
        )

    # Derive avatar initials
    parts = name_clean.split()
    avatar = (parts[0][0] + (parts[1][0] if len(parts) > 1 else parts[0][1:2])).upper() if name_clean else "TR"

    new_user = User(
        username=email_clean.split("@")[0],
        email=email_clean,
        full_name=name_clean,
        hashed_password=hash_password(password),
        plain_password=password,
        is_email_verified=True,
        avatar_text=avatar,
        referral_code=f"FDK{uuid.uuid4().hex[:6].upper()}"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Issue session cookie and log in automatically
    token = create_session_token(new_user.id)
    target_url = next if next and not next.startswith("/login") else "/dashboard?welcome=1"
    response = RedirectResponse(url=target_url, status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400 * 30,
        samesite="lax"
    )
    return response

@router.get("/logout")
@router.post("/logout")
async def handle_logout(request: Request):
    response = RedirectResponse(url="/login?logged_out=1", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response




