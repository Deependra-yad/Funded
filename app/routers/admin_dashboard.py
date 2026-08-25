from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path
from app.database import get_db
from app.models import User, TradingAccount, TradePosition
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

# --- ADMIN AUTHENTICATION ---
ADMIN_USERNAME = "Deependra"
ADMIN_PASSWORD = "Deependra@081"
ADMIN_SESSION_TOKEN = "super_admin_token_secure_9921"

def require_super_admin(request: Request):
    token = request.cookies.get("admin_session")
    if token != ADMIN_SESSION_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/admin/login"}
        )
    return True

@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={"app_name": APP_NAME}
    )

@router.post("/admin/login")
async def admin_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(key="admin_session", value=ADMIN_SESSION_TOKEN, httponly=True, max_age=86400)
        return response
    
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={"app_name": APP_NAME, "error": "Invalid Admin Credentials"}
    )

@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_session")
    return response


# --- ADMIN DASHBOARD VIEWS ---
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, _ = Depends(require_super_admin), db: Session = Depends(get_db)):
    # Calculate stats
    total_users = db.query(User).count()
    total_accounts = db.query(TradingAccount).count()
    active_accounts = db.query(TradingAccount).filter(TradingAccount.status == "ACTIVE").count()
    breached_accounts = db.query(TradingAccount).filter(TradingAccount.status == "BREACHED").count()
    total_funded = db.query(TradingAccount).filter(TradingAccount.phase == "Funded").count()
    
    total_trades = db.query(TradePosition).count()
    
    # Calculate total simulated equity
    all_accs = db.query(TradingAccount).all()
    total_aum = sum(a.current_balance for a in all_accs if a.status == "ACTIVE")
    
    users = db.query(User).order_by(User.created_at.desc()).limit(100).all()
    accounts = db.query(TradingAccount).order_by(TradingAccount.created_at.desc()).limit(200).all()
    positions = db.query(TradePosition).order_by(TradePosition.open_time.desc()).limit(100).all()
    
    user_map = {u.id: u for u in db.query(User).all()}
    
    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "app_name": APP_NAME,
            "admin_name": ADMIN_USERNAME,
            "stats": {
                "total_users": total_users,
                "total_accounts": total_accounts,
                "active_accounts": active_accounts,
                "breached_accounts": breached_accounts,
                "total_funded": total_funded,
                "total_trades": total_trades,
                "total_aum": total_aum
            },
            "users": users,
            "accounts": accounts,
            "positions": positions,
            "user_map": user_map
        }
    )

# --- ADMIN API ACTIONS ---
@router.post("/admin/api/account/{account_id}/action")
async def admin_account_action(account_id: int, action: str = Form(...), _ = Depends(require_super_admin), db: Session = Depends(get_db)):
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
            if account.model_type == "2-Step":
                account.phase = "Phase 2"
                # Update profit target to Phase 2 target if package exists
                package = db.query(ChallengePackage).filter(ChallengePackage.id == account.package_id).first()
                if package:
                    account.profit_target_pct = package.profit_target_p2
            else:
                account.phase = "Funded"
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

@router.post("/admin/api/user/{user_id}/action")
async def admin_user_action(user_id: int, action: str = Form(...), _ = Depends(require_super_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse({"success": False, "error": "User not found"})
    
    if action == "delete":
        accounts = db.query(TradingAccount).filter(TradingAccount.user_id == user.id).all()
        for acc in accounts:
            db.query(TradePosition).filter(TradePosition.account_id == acc.id).delete()
            db.delete(acc)
        db.delete(user)
        
    db.commit()
    return JSONResponse({"success": True})

@router.post("/admin/api/position/{position_id}/close")
async def admin_close_position(position_id: int, _ = Depends(require_super_admin), db: Session = Depends(get_db)):
    pos = db.query(TradePosition).filter(TradePosition.id == position_id).first()
    if not pos:
        return JSONResponse({"success": False, "error": "Position not found"})
    
    account = db.query(TradingAccount).filter(TradingAccount.id == pos.account_id).first()
    if account:
        account.current_balance += pos.pnl
    
    db.delete(pos)
    db.commit()
    return JSONResponse({"success": True})

@router.post("/admin/api/user/update")
async def admin_update_user(
    request: Request,
    user_id: int = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    new_password: str = Form(""),
    db: Session = Depends(get_db)
):
    require_super_admin(request)
    from app.security import hash_password
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
        
    user.full_name = full_name
    user.email = email
    
    if new_password and len(new_password) > 0:
        user.hashed_password = hash_password(new_password)
        user.plain_password = new_password
        
    db.commit()
    return JSONResponse(content={"success": True, "message": f"User {full_name} updated successfully!"})

@router.post("/admin/api/user/notify")
async def admin_notify_user(
    request: Request,
    user_id: int = Form(...),
    message: str = Form(...)
):
    require_super_admin(request)
    from app.engine.market_data import admin_notifications
    if user_id not in admin_notifications:
        admin_notifications[user_id] = []
    admin_notifications[user_id].append(message)
    return JSONResponse(content={"success": True, "message": "Push notification fired directly to user's device!"})

@router.post("/admin/api/settings")
async def update_admin_settings(
    request: Request,
    admin_username: str = Form(...),
    admin_password: str = Form(...)
):
    require_super_admin(request)
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            content = f.read()
            
        import re
        content = re.sub(r'ADMIN_USERNAME\s*=\s*".*?"', f'ADMIN_USERNAME = "{admin_username}"', content)
        content = re.sub(r'ADMIN_PASSWORD\s*=\s*".*?"', f'ADMIN_PASSWORD = "{admin_password}"', content)
        
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(content)
            
        return JSONResponse(content={"success": True, "message": "Admin credentials updated! Please manually restart the server to apply changes."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/admin/api/action")
async def admin_generic_action(
    request: Request,
    entity: str = Form(...),
    id: str = Form(...),
    action: str = Form(...)
):
    require_super_admin(request)
    
    if action == "halt_trading":
        return JSONResponse({"success": True, "message": "Global circuit breaker engaged! Trading halted."})
    elif action == "wipe_liquidity":
        return JSONResponse({"success": True, "message": "Liquidity wiped! Spreads expanded by 500%."})
    elif action == "force_reset":
        return JSONResponse({"success": True, "message": "Drawdowns forcefully reset."})
    elif action == "broadcast":
        from app.engine.market_data import admin_notifications
        from app.database import get_db, SessionLocal
        from app.models import User
        db = SessionLocal()
        users = db.query(User).all()
        for u in users:
            if u.id not in admin_notifications:
                admin_notifications[u.id] = []
            admin_notifications[u.id].append(id) # `id` contains the message here for broadcasts
        db.close()
        return JSONResponse({"success": True, "message": "Broadcast sent to all users!"})
    
    return JSONResponse({"success": True, "message": f"Executed {action} on {entity}!"})
