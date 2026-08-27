import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the 4 buttons by matching their data-lucide tags
content = re.sub(r'<button class="p-2 text-slate-400[^>]+>\s*<i data-lucide="receipt"[^>]+></i>\s*</button>', '', content)
content = re.sub(r'<button class="p-2 text-slate-400[^>]+>\s*<i data-lucide="shield"[^>]+></i>\s*</button>', '', content)
content = re.sub(r'<button class="p-2 text-slate-400[^>]+>\s*<i data-lucide="target"[^>]+></i>\s*</button>', '', content)
content = re.sub(r'<button class="p-2 text-slate-400[^>]+>\s*<i data-lucide="shopping-cart"[^>]+></i>\s*</button>', '', content)

with open('app/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
