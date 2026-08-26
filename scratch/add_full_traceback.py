import re

with open('app/routers/auth.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire handle_register body with a try-except
pattern = r'async def handle_register\([\s\S]*?\n\):([\s\S]*?)(?=@router\.get\("/logout"\))'

def replacer(match):
    body = match.group(1)
    # Remove the previous try-except that we injected
    body = body.replace('    try:\n', '')
    body = re.sub(r'    except Exception as e:\n        import traceback\n        return Response\(content=f"Error: \{e\}\\n\{traceback\.format_exc\(\)\}", status_code=500, media_type="text/plain"\)', '', body)
    
    lines = body.split('\n')
    indented = '\n'.join(['    ' + line if line else line for line in lines])
    
    return f'''async def handle_register(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    next: str = Form("/dashboard"),
    remember_me: str = Form(None),
    db: Session = Depends(get_db)
):
    try:{indented}
    except Exception as e:
        import traceback
        return Response(content=f"Error: {{e}}\\n{{traceback.format_exc()}}", status_code=500, media_type="text/plain")
'''

new_content = re.sub(pattern, replacer, content)

with open('app/routers/auth.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

