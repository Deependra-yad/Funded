from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, Certificate, TradingAccount, AppSetting
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/passed-challenges", response_class=HTMLResponse)
async def passed_challenges_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    certificates = db.query(Certificate).filter(Certificate.user_id == user.id).order_by(Certificate.issue_date.desc()).all()
    passed_accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id, TradingAccount.status == "PASSED").all()

    return templates.TemplateResponse(
        request=request,
        name="passed_challenges.html",
        context={
            "app_name": APP_NAME,
            "active_page": "passed_challenges",
            "user": user,
            "certificates": certificates,
            "passed_accounts": passed_accounts
        }
    )

@router.get("/certificate/{cert_id}", response_class=HTMLResponse)
async def view_certificate(request: Request, cert_id: str, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.cert_id == cert_id, Certificate.user_id == user.id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    setting = db.query(AppSetting).filter(AppSetting.key == 'director_name').first()
    director_name = setting.value if setting else "Deependra Yadav"

    return templates.TemplateResponse(
        request=request,
        name="certificate_view.html",
        context={
            "app_name": APP_NAME,
            "active_page": "passed_challenges",
            "user": user,
            "cert": cert,
            "director_name": director_name
        }
    )
