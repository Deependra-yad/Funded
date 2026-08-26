code = '''
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
'''

with open('app/routers/admin_dashboard.py', 'a', encoding='utf-8') as f:
    f.write(code)
print("Added settings endpoint.")

