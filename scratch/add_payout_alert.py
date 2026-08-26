with open('app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

alert_html = '''
    {% if request.query_params.get('payout_success') %}
    <div class="bg-emerald-50 border border-emerald-200 text-emerald-800 px-4 py-3 rounded-xl mb-6 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <div class="bg-emerald-100 p-1.5 rounded-full"><i data-lucide="check" class="w-4 h-4 text-emerald-600"></i></div>
            <div>
                <p class="font-bold text-sm">Payout Requested Successfully!</p>
                <p class="text-xs text-emerald-600">Your profit split is being processed and will be reviewed within 24 hours.</p>
            </div>
        </div>
        <button onclick="this.parentElement.style.display='none'" class="text-emerald-500 hover:text-emerald-700"><i data-lucide="x" class="w-4 h-4"></i></button>
    </div>
    {% endif %}
'''

html = html.replace('<!-- Stats Grid -->', alert_html + '<!-- Stats Grid -->')

with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

