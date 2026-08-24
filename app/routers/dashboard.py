from fastapi import APIRouter, Depends, Request
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
            "accounts": accounts,
            "active_accounts": active_accounts,
            "passed_accounts": passed_accounts,
            "breached_accounts": breached_accounts,
            "total_balance": round(total_balance, 2),
            "total_equity": round(total_equity, 2),
            "total_profit": round(total_profit, 2),
        }
    )
