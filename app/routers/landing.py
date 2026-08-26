from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.config import APP_NAME, APP_TAGLINE
from app.database import get_db
from app.models import ChallengePackage
from app.security import get_optional_user

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, user = Depends(get_optional_user), db: Session = Depends(get_db)):
    packages = db.query(ChallengePackage).order_by(ChallengePackage.price.asc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "app_name": APP_NAME,
            "app_tagline": APP_TAGLINE,
            "user": user,
            "packages": packages
        }
    )
