with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace button
content = content.replace(
    '''<button onclick="adminAction('global', '0', 'generate_promo')" class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-slate-600">Generate Master Promo</button>''',
    '''<button onclick="openPromoModal()" class="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-amber-500/20">Generate Master Promo</button>'''
)

promo_modal = """
    <div id="promoModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl">
            <div class="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-800/50">
                <h3 class="text-lg font-bold text-white flex items-center gap-2"><i data-lucide="tag" class="w-5 h-5 text-amber-500"></i> Generate Promo Code</h3>
            </div>
            <div class="p-6 space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Promo Code Name</label>
                    <input type="text" id="promoCodeInput" placeholder="e.g. SUMMER50" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-amber-500 outline-none uppercase font-mono">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Discount Percentage (%)</label>
                    <input type="number" id="promoDiscountInput" placeholder="50" min="1" max="100" class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-amber-500 outline-none">
                </div>
            </div>
            <div class="p-4 bg-slate-800/50 border-t border-slate-800 flex justify-end gap-3">
                <button onclick="closePromoModal()" class="px-4 py-2 rounded-xl text-slate-400 hover:bg-white/5 transition-colors">Cancel</button>
                <button onclick="savePromoCode()" class="bg-amber-600 hover:bg-amber-500 text-white px-6 py-2 rounded-xl font-bold transition-colors shadow-lg shadow-amber-500/20">Generate</button>
            </div>
        </div>
    </div>
"""

promo_js = """
        function openPromoModal() { document.getElementById('promoModal').classList.remove('hidden'); }
        function closePromoModal() { document.getElementById('promoModal').classList.add('hidden'); }
        function savePromoCode() {
            const code = document.getElementById('promoCodeInput').value.toUpperCase();
            const discount = document.getElementById('promoDiscountInput').value;
            if(!code || !discount) return;
            adminActionWithPayload('global', code, 'generate_promo', discount);
            closePromoModal();
        }
"""

if 'openPromoModal' not in content:
    content = content.replace('<!-- Modals -->', '<!-- Modals -->\n' + promo_modal)
    content = content.replace('function openSettingsModal', promo_js + '\n        function openSettingsModal')

    with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

