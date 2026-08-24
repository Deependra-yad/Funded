from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, AffiliateReferral
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/ib-program", response_class=HTMLResponse)
async def ib_program_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    referrals = db.query(AffiliateReferral).filter(AffiliateReferral.referrer_id == user.id).order_by(AffiliateReferral.created_at.desc()).all()

    total_commission = sum(r.commission_earned for r in referrals)
    paid_commission = sum(r.commission_earned for r in referrals if r.status == "PAID")
    pending_commission = sum(r.commission_earned for r in referrals if r.status == "PENDING")

    return templates.TemplateResponse(
        request=request,
        name="ib_program.html",
        context={
            "app_name": APP_NAME,
            "active_page": "ib_program",
            "user": user,
            "referrals": referrals,
            "total_referrals": len(referrals),
            "total_commission": round(total_commission, 2),
            "paid_commission": round(paid_commission, 2),
            "pending_commission": round(pending_commission, 2)
        }
    )
