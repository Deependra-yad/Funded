from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import User
from app.security import require_auth
from app.config import APP_NAME

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

FEATURE_CONTENT = {
    "heatmap": {
        "title": "Market Heatmap",
        "icon": "bar-chart",
        "desc": "Real-time visualization of market movers.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-crypto-coins-heatmap.js" async>{"dataSource": "Crypto","blockSize": "market_cap_calc","blockColor": "change","locale": "en","symbolUrl": "","colorTheme": "dark","hasTopBar": false,"isDataSetEnabled": false,"isZoomEnabled": true,"hasSymbolTooltip": true,"width": "100%","height": "100%"}</script></div>'''
    },
    "news": {
        "title": "Market News",
        "icon": "newspaper",
        "desc": "Latest fundamental news and economic updates.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>{"feedMode": "all_symbols","colorTheme": "dark","isTransparent": true,"displayMode": "regular","width": "100%","height": "100%","locale": "en"}</script></div>'''
    },
    "calendar": {
        "title": "Economic Calendar",
        "icon": "calendar",
        "desc": "Track key economic events and data releases.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>{"colorTheme": "dark","isTransparent": true,"width": "100%","height": "100%","locale": "en","importanceFilter": "-1,0,1"}</script></div>'''
    },
    "leaderboard": {
        "title": "Leaderboard",
        "icon": "flag",
        "desc": "Top funded traders this month.",
        "widget": "<div class='flex items-center justify-center h-64 text-slate-500'>Leaderboard data is currently syncing.</div>"
    }
}

@router.get("/feature/{name}", response_class=HTMLResponse)
async def view_feature(request: Request, name: str, user: User = Depends(require_auth)):
    feature = FEATURE_CONTENT.get(name, {
        "title": name.replace("-", " ").title(),
        "icon": "box",
        "desc": "This feature is currently being provisioned for your account.",
        "widget": "<div class='flex flex-col items-center justify-center h-64 text-slate-500'><i data-lucide='settings' class='w-12 h-12 mb-4 animate-spin-slow opacity-20'></i><p>Check back later.</p></div>"
    })
    
    return templates.TemplateResponse(
        request=request,
        name="feature.html",
        context={
            "app_name": APP_NAME,
            "user": user,
            "feature": feature
        }
    )
