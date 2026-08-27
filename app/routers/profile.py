from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/socials", response_class=HTMLResponse)
async def socials_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="socials.html",
        context={
            "app_name": APP_NAME,
            "active_page": "socials",
            "user": user
        }
    )

@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="socials.html",
        context={
            "app_name": APP_NAME,
            "active_page": "contact",
            "user": user
        }
    )

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "app_name": APP_NAME,
            "active_page": "profile",
            "user": user
        }
    )

@router.post("/profile/update")
async def update_profile(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    user.full_name = full_name
    user.email = email
    if len(full_name) > 0:
        parts = full_name.strip().split()
        user.avatar_text = (parts[0][0] + (parts[1][0] if len(parts) > 1 else parts[0][1:2])).upper()
    db.commit()
    return RedirectResponse(url="/profile?saved=1", status_code=303)

@router.post("/profile/delete-request")
async def request_deletion(request: Request, reason: str = Form(""), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    user.deletion_requested = True
    user.deletion_reason = reason
    db.commit()
    return RedirectResponse(url="/profile?deleted=1", status_code=303)
