with open('app/routers/auth.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Wrap db logic and cookie logic in try...except
pattern = r'(    new_user = User\([\s\S]*?samesite="lax"\n    \)\n    return response)'
replacement = r'''    try:
\1
    except Exception as e:
        import traceback
        return Response(content=f"Error: {e}\n{traceback.format_exc()}", status_code=500, media_type="text/plain")'''

# indent the matched group
def replacer(match):
    lines = match.group(1).split('\n')
    indented = '\n'.join(['        ' + line[4:] if line.startswith('    ') else line for line in lines])
    return f'''    try:
{indented}
    except Exception as e:
        import traceback
        return Response(content=f"Error: {{e}}\\n{{traceback.format_exc()}}", status_code=500, media_type="text/plain")'''

content = re.sub(pattern, replacer, content)

with open('app/routers/auth.py', 'w', encoding='utf-8') as f:
    f.write(content)

