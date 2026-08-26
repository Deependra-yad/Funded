with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
html = re.sub(r'setTimeout\(\(\) => \{[^\}]*toast\.remove\(\)[^\}]*\}, 3000\);',
              r"setTimeout(() => { toast.style.transform = 'translateY(-20px)'; toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 8000);",
              html)

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
