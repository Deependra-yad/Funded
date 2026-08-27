import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'alpinejs' not in content:
    content = content.replace('<script src="https://cdn.tailwindcss.com"></script>', '<script src="https://cdn.tailwindcss.com"></script>\n    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>')
    with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
