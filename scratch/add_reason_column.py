import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Reason column to Users table
content = content.replace(
    '<th class="px-4 py-3">Email</th>',
    '<th class="px-4 py-3">Email</th>\n                                    <th class="px-4 py-3 text-rose-300">Deletion Reason</th>'
)

user_row = """<td class="px-4 py-3 text-slate-400">{{ user.email }}</td>
                                    <td class="px-4 py-3 text-xs text-rose-300 max-w-[150px] truncate" title="{{ user.deletion_reason }}">{{ user.deletion_reason if user.deletion_requested else '-' }}</td>"""
content = content.replace('<td class="px-4 py-3 text-slate-400">{{ user.email }}</td>', user_row)

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

