with open('scratch/write_admin.py', 'r', encoding='utf-8') as f:
    html = f.read()
users_idx = html.find('id="tab-users"')
accounts_idx = html.find('id="tab-accounts"')
print(html[users_idx:accounts_idx][-200:])

