import re

with open('app/routers/dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

notif_endpoints = """
from fastapi.responses import JSONResponse

@router.get("/api/notifications")
async def get_notifications(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    # Global broadcast notifications have user_id = None
    notifs = db.query(Notification).filter(Notification.user_id.is_(None)).order_by(Notification.created_at.desc()).limit(10).all()
    return JSONResponse([
        {"id": n.id, "message": n.message, "created_at": n.created_at.isoformat()}
        for n in reversed(notifs)
    ])

@router.post("/api/notifications/{n_id}/dismiss")
async def dismiss_notification(n_id: int, request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    # A real system would track dismissed per user, but for now we just return success
    return JSONResponse({"success": True})
"""

if '/api/notifications' not in content:
    content = content.replace('router = APIRouter()', 'router = APIRouter()\n' + notif_endpoints)
    with open('app/routers/dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)

