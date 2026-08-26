import re
with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()
match = re.search(r'<div class="sticky top-0.*?</header>', html, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")

