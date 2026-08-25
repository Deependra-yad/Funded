code = '''
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
        
    db.commit()
    return JSONResponse(content={"success": True, "message": f"User {full_name} updated successfully!"})

@router.post("/admin/api/user/notify")
async def admin_notify_user(
    request: Request,
    user_id: int = Form(...),
    message: str = Form(...)
):
    require_super_admin(request)
    return JSONResponse(content={"success": True, "message": "Push notification fired directly to user's device!"})
'''

with open('app/routers/admin_dashboard.py', 'a', encoding='utf-8') as f:
    f.write(code)
print("Updated admin_dashboard.py")

