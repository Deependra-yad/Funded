import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Navigation Button for Content Management
nav_content = '''<button onclick="switchTab('content')" id="nav-content" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
                <i data-lucide="edit-3" class="w-4 h-4 text-pink-400"></i> Content Management
            </button>'''

if 'id="nav-content"' not in content:
    content = content.replace('id="nav-chat"', 'id="nav-chat"').replace('Live Support Chat\n            </button>', 'Live Support Chat\n            </button>\n            ' + nav_content)


# 2. Add Content Management Tab
tab_content = '''
        <div id="tab-content" class="tab-content window-mode space-y-6">
            <div class="window-header">
                <h2 class="text-sm font-bold flex items-center gap-2 text-white"><i data-lucide="edit-3" class="w-4 h-4 text-pink-400"></i> Content Management</h2>
                <div class="flex gap-2">
                    <button onclick="this.closest('.tab-content').classList.remove('window-mode'); document.getElementById('window-overlay').classList.add('hidden')" title="Minimize" class="w-3.5 h-3.5 rounded-full bg-amber-500 hover:bg-amber-400 flex items-center justify-center"></button>
                    <button onclick="this.closest('.tab-content').classList.toggle('window-mode')" title="Maximize" class="w-3.5 h-3.5 rounded-full bg-emerald-500 hover:bg-emerald-400 flex items-center justify-center"></button>
                    <button onclick="this.closest('.tab-content').classList.remove('window-mode'); document.getElementById('window-overlay').classList.add('hidden')" title="Close" class="w-3.5 h-3.5 rounded-full bg-rose-500 hover:bg-rose-400 flex items-center justify-center"></button>
                </div>
            </div>
            <div class="p-6 h-full flex flex-col">
                <h3 class="text-xl font-bold text-white mb-4">Edit Dynamic Pages</h3>
                <div class="grid grid-cols-1 gap-4 mb-4">
                    <select id="content-page-select" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-pink-500 outline-none">
                        <option value="page_affiliate">Affiliate Program</option>
                        <option value="page_support">Support Center</option>
                        <option value="page_coupons">Coupon Codes</option>
                        <option value="page_giveaway">FundedFirm Giveaway</option>
                        <option value="page_comparison">Account Comparison</option>
                        <option value="page_rules">Trading Rules</option>
                        <option value="page_privacy">Data & Privacy</option>
                    </select>
                </div>
                <div class="flex-1 flex flex-col gap-4">
                    <input type="text" id="content-title" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-pink-500 outline-none" placeholder="Page Title (e.g. Trading Rules)">
                    <input type="text" id="content-desc" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-pink-500 outline-none" placeholder="Description">
                    <input type="text" id="content-icon" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-pink-500 outline-none" placeholder="Lucide Icon name (e.g. clipboard-list)">
                    <textarea id="content-html" class="flex-1 w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white focus:border-pink-500 outline-none font-mono text-xs" placeholder="HTML Widget Code..."></textarea>
                </div>
                <div class="mt-4 flex justify-end">
                    <button onclick="saveDynamicPage()" class="bg-pink-600 hover:bg-pink-500 text-white font-bold py-3 px-6 rounded-lg transition-colors">Save Page Content</button>
                </div>
            </div>
        </div>
'''

if 'id="tab-content"' not in content:
    content = content.replace('<div id="window-overlay"', tab_content + '\n    <div id="window-overlay"')
    
# 3. Add JS function to save it
js = '''
        function saveDynamicPage() {
            const pageKey = document.getElementById('content-page-select').value;
            const title = document.getElementById('content-title').value;
            const desc = document.getElementById('content-desc').value;
            const icon = document.getElementById('content-icon').value;
            const html = document.getElementById('content-html').value;
            
            const payload = JSON.stringify({
                title: title,
                desc: desc,
                icon: icon,
                widget: html
            });
            
            adminActionWithPayload('system', pageKey, 'update_setting', payload);
        }
'''
if 'saveDynamicPage()' not in content:
    content = content.replace('function openSettingsModal', js + '\n        function openSettingsModal')

# 4. We also need to map the titles in switchTab
if "'settings': 'Platform Settings'" in content and "'content': 'Content Management'" not in content:
    content = content.replace("'settings': 'Platform Settings'", "'settings': 'Platform Settings',\n            'content': 'Content Management'")

with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("CONTENT TAB ADDED")
