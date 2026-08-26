with open('app/routers/trading.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
start = -1
for i, line in enumerate(lines):
    if '@router.get("/api/account/{account_id}/state")' in line:
        start = i
if start != -1:
    print(''.join(lines[start:start+70]))

