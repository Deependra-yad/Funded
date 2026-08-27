import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make all tabs behave like Windows Tabs
tab_headers = [
    ("users", "User Management", "users", "indigo-400"),
    ("accounts", "Trading Accounts", "briefcase", "blue-400"),
    ("trades", "Live Market Trades", "activity", "rose-400"),
    ("rules", "Prop Firm Rules", "shield", "emerald-400"),
    ("payouts", "Payout Requests", "dollar-sign", "amber-400"),
    ("operations", "Market Operations", "alert-triangle", "rose-500"),
    ("settings", "Platform Settings", "settings", "slate-400"),
]

for tab_id, title, icon, color in tab_headers:
    old_header = f'<h2 class="text-2xl font-bold mb-6 flex items-center gap-2"><i data-lucide="{icon}" class="w-6 h-6 text-{color}"></i> {title}</h2>'
    new_header = f'''
        <div class="flex justify-between items-center mb-6 pb-2 border-b border-slate-800 bg-slate-900/80 p-3 rounded-t-xl cursor-move handle">
            <h2 class="text-xl font-bold flex items-center gap-2"><i data-lucide="{icon}" class="w-5 h-5 text-{color}"></i> {title}</h2>
            <div class="flex gap-3">
                <button onclick="this.closest('.tab-content').classList.toggle('window-mode')" title="Minimize/Maximize" class="w-3.5 h-3.5 rounded-full bg-emerald-500 hover:bg-emerald-400 flex items-center justify-center transition-transform hover:scale-110"></button>
                <button onclick="this.closest('.tab-content').classList.toggle('window-mode')" title="Restore" class="w-3.5 h-3.5 rounded-full bg-amber-500 hover:bg-amber-400 flex items-center justify-center transition-transform hover:scale-110"></button>
                <button onclick="switchTab('overview')" title="Close" class="w-3.5 h-3.5 rounded-full bg-rose-500 hover:bg-rose-400 flex items-center justify-center transition-transform hover:scale-110"></button>
            </div>
        </div>
    '''
    content = content.replace(old_header, new_header)

# Make sure all tab contents have relative position so window-mode works
content = content.replace('class="tab-content custom-scrollbar overflow-y-auto h-full pb-20"', 'class="tab-content custom-scrollbar overflow-y-auto h-full pb-20 relative"')
content = content.replace('class="tab-content active custom-scrollbar overflow-y-auto h-full pb-20"', 'class="tab-content active custom-scrollbar overflow-y-auto h-full pb-20 relative"')

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
