from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, TradingAccount, TradePosition
from app.security import require_auth
from app.engine.prop_rules import evaluate_account_and_trades
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/challenges", response_class=HTMLResponse)
async def challenges_list(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id).order_by(TradingAccount.created_at.desc()).all()
    
    for acc in accounts:
        if acc.status == "ACTIVE":
            evaluate_account_and_trades(db, acc)

    return templates.TemplateResponse(
        request=request,
        name="challenges.html",
        context={
            "app_name": APP_NAME,
            "active_page": "challenges",
            "user": user,
            "accounts": accounts
        }
    )

@router.get("/challenges/{account_id}", response_class=HTMLResponse)
async def challenge_detail(request: Request, account_id: int, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.status == "ACTIVE":
        evaluate_account_and_trades(db, account)

    trades = db.query(TradePosition).filter(TradePosition.account_id == account.id).order_by(TradePosition.open_time.desc()).all()

    # Calculate statistics
    closed_trades = [t for t in trades if t.status == "CLOSED"]
    winning_trades = [t for t in closed_trades if t.pnl > 0]
    losing_trades = [t for t in closed_trades if t.pnl < 0]
    
    win_rate = round((len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0.0, 1)
    total_gain = sum(t.pnl for t in winning_trades)
    total_loss = abs(sum(t.pnl for t in losing_trades))
    profit_factor = round((total_gain / total_loss) if total_loss > 0 else (total_gain if total_gain > 0 else 1.0), 2)
    avg_win = round((total_gain / len(winning_trades)) if winning_trades else 0.0, 2)
    avg_loss = round((total_loss / len(losing_trades)) if losing_trades else 0.0, 2)

    return templates.TemplateResponse(
        request=request,
        name="challenge_detail.html",
        context={
            "app_name": APP_NAME,
            "active_page": "challenges",
            "user": user,
            "account": account,
            "trades": trades,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "total_trades": len(closed_trades)
        }
    )
