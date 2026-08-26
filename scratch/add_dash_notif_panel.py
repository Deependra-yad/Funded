with open('app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

notif_html = '''
    <!-- Notifications Panel -->
    <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm mb-6">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center gap-2">
            <i data-lucide="bell" class="w-5 h-5 text-indigo-600"></i>
            <h2 class="font-extrabold text-lg text-slate-900 tracking-tight">Recent Notifications</h2>
        </div>
        <div class="divide-y divide-slate-100">
            {% for n in notifications %}
            <div class="px-6 py-4 hover:bg-slate-50 transition-colors">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-bold px-2 py-0.5 rounded {% if n.type == 'success' %}bg-emerald-100 text-emerald-700{% elif n.type == 'warning' %}bg-amber-100 text-amber-700{% elif n.type == 'error' %}bg-rose-100 text-rose-700{% else %}bg-blue-100 text-blue-700{% endif %} uppercase tracking-wider mb-1 inline-block">
                        {{ n.type }}
                    </span>
                    <span class="text-xs text-slate-400 font-semibold">{{ n.created_at.strftime('%b %d, %H:%M') }}</span>
                </div>
                <p class="text-sm font-semibold text-slate-700 mt-1">{{ n.message }}</p>
            </div>
            {% endfor %}
            {% if notifications|length == 0 %}
            <div class="px-6 py-8 text-center text-slate-500 font-semibold text-sm">
                No recent notifications.
            </div>
            {% endif %}
        </div>
    </div>
'''

html = html.replace('<!-- Stats Grid -->', notif_html + '\n    <!-- Stats Grid -->')

with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
