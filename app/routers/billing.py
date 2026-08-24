from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import get_db
from app.models import User, Order
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/orders", response_class=HTMLResponse)
@router.get("/billing", response_class=HTMLResponse)
async def orders_and_billing(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
    total_spent = sum(o.amount_paid for o in orders if o.status == "COMPLETED")

    is_billing = "billing" in request.url.path
    page_name = "billing" if is_billing else "orders"

    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={
            "app_name": APP_NAME,
            "active_page": page_name,
            "user": user,
            "orders": orders,
            "total_spent": round(total_spent, 2)
        }
    )
