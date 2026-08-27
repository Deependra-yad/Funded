import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Windows-style headers to all tab-content sections
tabs = [
    ("tab-overview", "Platform Overview", "layout-dashboard", "slate-100"),
    ("tab-users", "Registered Users", "users", "indigo-400"),
    ("tab-accounts", "Trading Accounts", "briefcase", "blue-400"),
    ("tab-packages", "Challenge Packages", "package", "purple-400"),
    ("tab-trades", "Live Market Trades", "activity", "rose-400"),
    ("tab-rules", "Prop Firm Rules", "shield", "emerald-400"),
    ("tab-payouts", "Payout Requests", "dollar-sign", "amber-400"),
    ("tab-ops", "Market Operations", "alert-triangle", "rose-500"),
    ("tab-settings", "Platform Settings", "settings", "slate-400")
]

# We need to add the CSS for window-mode
css = """
    <style>
        .window-mode {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 85vw !important;
            height: 85vh !important;
            z-index: 100 !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
            border-radius: 0.75rem !important;
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            resize: both;
            overflow: auto;
            display: flex !important;
            flex-direction: column !important;
        }
        .window-mode .window-header {
            display: flex !important;
        }
        .window-header {
            display: none; /* hidden by default in normal mode */
            cursor: move;
            background: #1e293b;
            padding: 10px 16px;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #334155;
            flex-shrink: 0;
        }
    </style>
"""

if "<style>" not in content:
    content = content.replace("</head>", f"{css}\n</head>")

for tab_id, title, icon, color in tabs:
    # Find the <div id="tab-id" class="tab-content ...">
    pattern = rf'(<div id="{tab_id}" class="tab-content[^>]*>)'
    
    header = f'''
        <div class="window-header">
            <h2 class="text-sm font-bold flex items-center gap-2 text-white"><i data-lucide="{icon}" class="w-4 h-4 text-{color}"></i> {title}</h2>
            <div class="flex gap-2">
                <button onclick="this.closest('.tab-content').classList.remove('window-mode'); document.getElementById('window-overlay').classList.add('hidden')" title="Minimize" class="w-3.5 h-3.5 rounded-full bg-amber-500 hover:bg-amber-400 flex items-center justify-center"></button>
                <button onclick="this.closest('.tab-content').classList.toggle('window-mode')" title="Maximize" class="w-3.5 h-3.5 rounded-full bg-emerald-500 hover:bg-emerald-400 flex items-center justify-center"></button>
                <button onclick="this.closest('.tab-content').classList.remove('window-mode'); document.getElementById('window-overlay').classList.add('hidden')" title="Close" class="w-3.5 h-3.5 rounded-full bg-rose-500 hover:bg-rose-400 flex items-center justify-center"></button>
            </div>
        </div>
    '''
    
    # We want to insert the header right after the tab-content div opening tag
    if 'window-header' not in content:
        content = re.sub(pattern, r'\1\n' + header, content)

# Inject window overlay
if 'id="window-overlay"' not in content:
    content = content.replace('<div id="notify-user-modal"', '<div id="window-overlay" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 hidden"></div>\n    <div id="notify-user-modal"')

# Update sidebar switchTab function to open in window mode instead of normal tabs
content = content.replace('''function switchTab(tabId, title) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            if (title) document.getElementById('page-title').textContent = title;
        }''', '''function switchTab(tabId, title) {
            document.getElementById('window-overlay').classList.remove('hidden');
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.classList.remove('window-mode');
            });
            let tab = document.getElementById('tab-' + tabId);
            tab.classList.add('active');
            tab.classList.add('window-mode');
            if (title) document.getElementById('page-title').textContent = title;
        }''')


# 2. Master Promo Editable
content = content.replace('''<button onclick="adminAction('global', '0', 'generate_promo')" class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-600">Generate Master Promo</button>''', 
                          '''<button onclick="openPromoModal()" class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-600">Generate Master Promo</button>''')

promo_modal = """
    <div id="promoModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-white/10 rounded-2xl p-6 w-full max-w-lg">
            <h3 class="text-xl font-bold text-white mb-4">Generate Master Promo</h3>
            <input type="text" id="promoCodeInput" class="w-full bg-black/50 border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:border-primary mb-4" placeholder="Promo Code (e.g. SUMMER50)">
            <input type="number" id="promoDiscountInput" class="w-full bg-black/50 border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:border-primary mb-4" placeholder="Discount % (e.g. 50)">
            <div class="flex justify-end gap-3">
                <button onclick="closePromoModal()" class="px-4 py-2 rounded-xl text-slate-400 hover:bg-white/5 transition-colors">Cancel</button>
                <button onclick="generateCustomPromo()" class="px-4 py-2 rounded-xl bg-primary text-white font-bold hover:bg-primary/80 transition-colors">Generate</button>
            </div>
        </div>
    </div>
"""

promo_js = """
        function openPromoModal() { document.getElementById('promoModal').classList.remove('hidden'); }
        function closePromoModal() { document.getElementById('promoModal').classList.add('hidden'); }
        function generateCustomPromo() {
            const code = document.getElementById('promoCodeInput').value;
            const discount = document.getElementById('promoDiscountInput').value;
            if(!code || !discount) { showToast('Please fill all fields', 'error'); return; }
            adminActionWithPayload('global', code, 'generate_promo', discount);
            closePromoModal();
        }
"""

if 'id="promoModal"' not in content:
    content = content.replace('<!-- Modals -->', '<!-- Modals -->\n' + promo_modal)
    content = content.replace('function openSettingsModal', promo_js + '\n        function openSettingsModal')


# 3. Edit Capital Prices
package_edit_button = """
                            <button type="button" onclick="openPackageEditModal({{ pkg.id }}, '{{ pkg.price }}')" class="text-indigo-400 hover:text-indigo-300 mr-2"><i data-lucide="edit" class="w-4 h-4"></i></button>
"""
if 'openPackageEditModal' not in content:
    content = content.replace('<button type="submit" class="text-rose-400 hover:text-rose-300">', package_edit_button + '<button type="submit" class="text-rose-400 hover:text-rose-300">')

package_modal = """
    <div id="packageEditModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-white/10 rounded-2xl p-6 w-full max-w-lg">
            <h3 class="text-xl font-bold text-white mb-4">Edit Capital Price</h3>
            <input type="hidden" id="editPkgId">
            <label class="text-slate-400 text-sm mb-1 block">New Price (₹)</label>
            <input type="number" step="0.01" id="editPkgPrice" class="w-full bg-black/50 border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:border-primary mb-4">
            <div class="flex justify-end gap-3">
                <button onclick="closePackageEditModal()" class="px-4 py-2 rounded-xl text-slate-400 hover:bg-white/5 transition-colors">Cancel</button>
                <button onclick="savePackagePrice()" class="px-4 py-2 rounded-xl bg-primary text-white font-bold hover:bg-primary/80 transition-colors">Save Details</button>
            </div>
        </div>
    </div>
"""

package_js = """
        function openPackageEditModal(id, price) { 
            document.getElementById('editPkgId').value = id;
            document.getElementById('editPkgPrice').value = price;
            document.getElementById('packageEditModal').classList.remove('hidden'); 
        }
        function closePackageEditModal() { document.getElementById('packageEditModal').classList.add('hidden'); }
        function savePackagePrice() {
            const id = document.getElementById('editPkgId').value;
            const price = document.getElementById('editPkgPrice').value;
            if(!price) return;
            adminActionWithPayload('package', id, 'update_price', price);
            closePackageEditModal();
        }
"""
if 'id="packageEditModal"' not in content:
    content = content.replace('<!-- Modals -->', '<!-- Modals -->\n' + package_modal)
    content = content.replace('function openSettingsModal', package_js + '\n        function openSettingsModal')

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("INJECTED OK")
