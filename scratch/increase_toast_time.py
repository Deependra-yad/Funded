with open('app/templates/trading_terminal.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
html = re.sub(r'setTimeout\(\(\) => \{ toast\.style\.animation = \'slideOut 0\.3s ease forwards\'; setTimeout\(\(\) => toast\.remove\(\), 300\); \}, 3000\);',
              r"setTimeout(() => { toast.style.animation = 'slideOut 0.3s ease forwards'; setTimeout(() => toast.remove(), 300); }, 8000);",
              html)

with open('app/templates/trading_terminal.html', 'w', encoding='utf-8') as f:
    f.write(html)
