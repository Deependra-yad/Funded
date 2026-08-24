from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path
from app.database import get_db
from app.models import User, TradingAccount, TradePosition
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

# Simple admin check (in a real app, verify is_admin flag)
def require_admin(user: User = Depends(require_auth)):
    # For this demo, all authenticated users can view admin panel
    return user

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    # Calculate stats
    total_users = db.query(User).count()
    total_accounts = db.query(TradingAccount).count()
    active_accounts = db.query(TradingAccount).filter(TradingAccount.status == "ACTIVE").count()
    breached_accounts = db.query(TradingAccount).filter(TradingAccount.status == "BREACHED").count()
    total_funded = db.query(TradingAccount).filter(TradingAccount.phase == "Funded").count()
    
    total_trades = db.query(TradePosition).count()
    
    users = db.query(User).order_by(User.created_at.desc()).limit(50).all()
    accounts = db.query(TradingAccount).order_by(TradingAccount.created_at.desc()).limit(100).all()
    positions = db.query(TradePosition).order_by(TradePosition.open_time.desc()).limit(50).all()
    
    # Preload user references
    user_map = {u.id: u for u in db.query(User).all()}
    
    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "app_name": APP_NAME,
            "admin": admin,
            "stats": {
                "total_users": total_users,
                "total_accounts": total_accounts,
                "active_accounts": active_accounts,
                "breached_accounts": breached_accounts,
                "total_funded": total_funded,
                "total_trades": total_trades
            },
            "users": users,
            "accounts": accounts,
            "positions": positions,
            "user_map": user_map
        }
    )

@router.post("/admin/api/account/{account_id}/action")
async def admin_account_action(account_id: int, action: str = Form(...), db: Session = Depends(get_db)):
    account = db.query(TradingAccount).filter(TradingAccount.id == account_id).first()
    if not account:
        return JSONResponse({"success": False, "error": "Account not found"})
        
    if action == "reset":
        account.current_balance = account.initial_balance
        account.current_equity = account.initial_balance
        account.daily_starting_equity = account.initial_balance
        account.highest_recorded_equity = account.initial_balance
        account.status = "ACTIVE"
        account.phase = "Phase 1"
        account.breach_reason = None
        db.query(TradePosition).filter(TradePosition.account_id == account_id).delete()
        
    elif action == "pass_phase":
        if account.phase == "Phase 1":
            account.phase = "Phase 2"
        elif account.phase == "Phase 2":
            account.phase = "Funded"
        account.status = "ACTIVE"
        account.breach_reason = None
        
    elif action == "force_breach":
        account.status = "BREACHED"
        account.breach_reason = "Admin Forced Breach"
        
    elif action == "delete":
        db.query(TradePosition).filter(TradePosition.account_id == account_id).delete()
        db.delete(account)
        
    db.commit()
    return JSONResponse({"success": True})

@router.post("/admin/api/user/{user_id}/delete")
async def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse({"success": False, "error": "User not found"})
    
    # Delete all associated accounts and trades
    accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id).all()
    for acc in accounts:
        db.query(TradePosition).filter(TradePosition.account_id == acc.id).delete()
        db.delete(acc)
    
    db.delete(user)
    db.commit()
    return JSONResponse({"success": True})

@router.post("/admin/api/position/{position_id}/close")
async def admin_close_position(position_id: int, db: Session = Depends(get_db)):
    pos = db.query(TradePosition).filter(TradePosition.id == position_id).first()
    if not pos:
        return JSONResponse({"success": False, "error": "Position not found"})
    
    # In a real system, we'd calculate final PNL here based on live market.
    # For admin force close, we'll just delete it or mark it closed at current PNL.
    # To keep it simple, we just delete it from active positions and credit the balance.
    account = db.query(TradingAccount).filter(TradingAccount.id == pos.account_id).first()
    if account:
        account.current_balance += pos.pnl
    
    db.delete(pos)
    db.commit()
    return JSONResponse({"success": True})
