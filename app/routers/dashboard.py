from app.models import Notification
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, TradingAccount, ChallengePackage, Certificate
from app.security import require_auth
from app.engine.prop_rules import evaluate_account_and_trades
from app.config import APP_NAME, APP_TAGLINE

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id).all()
    notifications = db.query(Notification).filter(Notification.user_id.is_(None)).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Evaluate live metrics for active accounts
    for acc in accounts:
        if acc.status == "ACTIVE":
            evaluate_account_and_trades(db, acc)

    active_accounts = [a for a in accounts if a.status == "ACTIVE"]
    passed_accounts = [a for a in accounts if a.status == "PASSED"]
    breached_accounts = [a for a in accounts if a.status == "BREACHED"]

    # Calculate summary stats
    total_balance = sum(a.current_balance for a in accounts)
    total_equity = sum(a.current_equity for a in accounts)
    total_profit = sum(a.current_profit for a in accounts)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "app_name": APP_NAME,
            "app_tagline": APP_TAGLINE,
            "active_page": "dashboard",
            "user": user,
            "accounts": accounts, "notifications": notifications,
            "active_accounts": active_accounts,
            "passed_accounts": passed_accounts,
            "breached_accounts": breached_accounts,
            "total_balance": round(total_balance, 2),
            "total_equity": round(total_equity, 2),
            "total_profit": round(total_profit, 2),
        }
    )


@router.post("/api/payout/request")
async def request_payout(account_id: int = Form(...), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if not account or account.phase != "Funded":
        raise HTTPException(status_code=400, detail="Invalid account for payout")
    
    if account.current_profit <= 0:
        raise HTTPException(status_code=400, detail="No profits available for payout")
        
    # Mock payout deduction
    payout_amt = account.current_profit
    account.current_balance -= payout_amt
    account.current_equity -= payout_amt
    db.commit()
    
    return RedirectResponse(url="/dashboard?payout_success=1", status_code=303)

from fastapi.responses import JSONResponse, RedirectResponse

@router.post("/api/notifications/{notif_id}/dismiss")
async def dismiss_notification(notif_id: int, request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        return JSONResponse({"success": False})
    
    # Delete the notification
    db.delete(notif)
    db.commit()
    
    return JSONResponse({"success": True})

@router.get("/api/notifications")
async def get_notifications(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(
        (Notification.user_id == user.id) | (Notification.user_id.is_(None))
    ).order_by(Notification.created_at.desc()).limit(20).all()
    
    return JSONResponse([
        {"id": n.id, "message": n.message, "type": n.type if hasattr(n, 'type') else "info", "created_at": n.created_at.isoformat() if n.created_at else ""}
        for n in notifications
    ])
