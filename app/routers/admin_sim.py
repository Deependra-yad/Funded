from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, TradingAccount, TradePosition
from app.security import require_auth
from app.engine.prop_rules import evaluate_account_and_trades
from app.engine.market_data import market_engine
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/admin/simulator", response_class=HTMLResponse)
async def admin_simulator_page(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id).all()
    return templates.TemplateResponse(
        request=request,
        name="admin_sim.html",
        context={
            "app_name": APP_NAME,
            "active_page": "admin_sim",
            "user": user,
            "accounts": accounts
        }
    )

@router.post("/admin/sim/pass-account")
async def sim_pass_account(account_id: int = Form(...), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if account:
        target_amt = account.initial_balance * (account.profit_target_pct / 100.0) + 200.0
        account.current_balance = account.initial_balance + target_amt
        account.current_equity = account.current_balance
        account.days_traded = max(account.days_traded, account.min_trading_days)
        account.status = "ACTIVE"
        evaluate_account_and_trades(db, account)
    return RedirectResponse(url=f"/challenges/{account_id}", status_code=303)

@router.post("/admin/sim/breach-account")
async def sim_breach_account(account_id: int = Form(...), breach_type: str = Form("daily"), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if account:
        if breach_type == "daily":
            loss_amt = account.daily_starting_equity * (account.max_daily_loss_pct / 100.0) + 100.0
            account.current_balance -= loss_amt
            account.current_equity = account.current_balance
        else:
            loss_amt = account.initial_balance * (account.max_total_loss_pct / 100.0) + 100.0
            account.current_balance = account.initial_balance - loss_amt
            account.current_equity = account.current_balance
        
        account.status = "ACTIVE"
        evaluate_account_and_trades(db, account)
    return RedirectResponse(url=f"/challenges/{account_id}", status_code=303)

@router.post("/admin/sim/reset-account")
async def sim_reset_account(account_id: int = Form(...), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id, TradingAccount.user_id == user.id).first()
    if account:
        account.current_balance = account.initial_balance
        account.current_equity = account.initial_balance
        account.daily_starting_equity = account.initial_balance
        account.highest_recorded_equity = account.initial_balance
        account.status = "ACTIVE"
        account.phase = "Phase 1"
        account.breach_reason = None
        account.days_traded = 1
        db.query(TradePosition).filter(TradePosition.account_id == account.id).delete()
        db.commit()
    return RedirectResponse(url=f"/challenges/{account_id}", status_code=303)

@router.post("/admin/sim/market-spike")
async def sim_market_spike(symbol: str = Form("XAUUSD"), pips: float = Form(50.0), user: User = Depends(require_auth)):
    if symbol in market_engine.prices:
        cfg = market_engine.prices[symbol]
        step = pips * 0.1
        cfg["mid"] += step
        cfg["bid"] += step
        cfg["ask"] += step
    return JSONResponse(content={"success": True, "symbol": symbol, "new_price": market_engine.prices.get(symbol)})
