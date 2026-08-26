with open('app/routers/auth.py', 'r', encoding='utf-8') as f:
    content = f.read()

endpoint_code = '''
@router.post("/profile/delete-request")
async def request_account_deletion(request: Request, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    user.deletion_requested = True
    db.commit()
    return RedirectResponse(url="/profile?delete_requested=1", status_code=303)
'''

content += '\n' + endpoint_code

with open('app/routers/auth.py', 'w', encoding='utf-8') as f:
    f.write(content)
