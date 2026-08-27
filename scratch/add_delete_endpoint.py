with open('app/routers/profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

delete_route = """
@router.post("/profile/delete-request")
async def request_deletion(request: Request, reason: str = Form(""), user: User = Depends(require_auth), db: Session = Depends(get_db)):
    user.deletion_requested = True
    user.deletion_reason = reason
    db.commit()
    return RedirectResponse(url="/profile?deleted=1", status_code=303)
"""

if 'def request_deletion' not in content:
    content += delete_route

with open('app/routers/profile.py', 'w', encoding='utf-8') as f:
    f.write(content)

