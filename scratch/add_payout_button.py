with open('app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

payout_btn = '''
                    {% if acc.phase == 'Funded' %}
                    <form action="/api/payout/request" method="POST" class="inline" onsubmit="return confirm('Request payout for current profits?');">
                        <input type="hidden" name="account_id" value="{{ acc.id }}">
                        <button type="submit" class="bg-emerald-100 hover:bg-emerald-200 text-emerald-800 font-extrabold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 transition-colors">
                            <i data-lucide="banknote" class="w-3.5 h-3.5"></i> Payout
                        </button>
                    </form>
                    {% endif %}
'''

html = html.replace('<span>Metrics</span>\n                            </a>', '<span>Metrics</span>\n                            </a>' + payout_btn)

with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

