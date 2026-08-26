with open('app/templates/orders.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Action header
html = html.replace('<th class="py-3 px-4">Date</th>', '<th class="py-3 px-4">Date</th>\n                        <th class="py-3 px-4 text-right">Action</th>')

# Add Download button
button_html = '''<td class="py-3 px-4 text-slate-400 font-sans text-[11px]">{{ o.created_at.strftime('%b %d, %Y') }}</td>
                        <td class="py-3 px-4 text-right">
                            <a href="/api/orders/{{ o.id }}/receipt" target="_blank" class="text-xs font-bold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded transition-colors inline-flex items-center gap-1">
                                <i data-lucide="download" class="w-3 h-3"></i> Receipt
                            </a>
                        </td>'''
html = html.replace('<td class="py-3 px-4 text-slate-400 font-sans text-[11px]">{{ o.created_at.strftime(\'%b %d, %Y\') }}</td>', button_html)

with open('app/templates/orders.html', 'w', encoding='utf-8') as f:
    f.write(html)

