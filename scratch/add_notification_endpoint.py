with open('app/routers/dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

fetch_endpoint = """
@router.get("/api/notifications")
async def get_notifications(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse([])
    
    notifications = db.query(Notification).filter(
        (Notification.user_id == user.id) | (Notification.user_id == None)
    ).order_by(Notification.created_at.desc()).all()
    
    return JSONResponse([
        {"id": n.id, "message": n.message, "created_at": n.created_at.isoformat()}
        for n in notifications
    ])
"""
if 'def get_notifications' not in content:
    content += fetch_endpoint

with open('app/routers/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

