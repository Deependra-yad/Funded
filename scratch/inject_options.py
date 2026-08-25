import os

TARGET = r'p:\Python\scratch\inject_options.py'

script = r'''with open('app/templates/trading_terminal.html', 'r') as f:
    content = f.read()

# 1. Add "Option Chain" button to the Watchlist Panel (above the list)
button_html = """            <div class="px-4 py-2 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
                <span class="text-xs font-bold text-slate-500 uppercase">Instruments</span>
                <button onclick="openOptionChain()" class="text-[10px] bg-indigo-50 text-indigo-600 hover:bg-indigo-100 px-2 py-1 rounded font-bold transition-colors border border-indigo-200 flex items-center gap-1">
                    <i data-lucide="layers" class="w-3 h-3"></i> Option Chain
                </button>
            </div>
            <div class="flex-1 overflow-y-auto">"""

content = content.replace(
    '''            <div class="px-4 py-2 bg-slate-50 border-b border-slate-200">
                <span class="text-xs font-bold text-slate-500 uppercase">Watchlist</span>
            </div>
            <div class="flex-1 overflow-y-auto">''',
    button_html
)


# 2. Add the Option Chain Modal HTML right before closing </body>
modal_html = """
    <!-- Option Chain Modal -->
    <div id="option-chain-modal" class="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-[100] hidden flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-6xl h-[85vh] rounded-xl shadow-2xl flex flex-col overflow-hidden border border-slate-200">
            <!-- Header -->
            <div class="h-14 bg-slate-900 flex items-center justify-between px-6 shrink-0">
                <div class="flex items-center gap-4">
                    <h2 class="text-white font-bold text-lg flex items-center gap-2"><i data-lucide="layers" class="w-5 h-5 text-indigo-400"></i> Advanced Option Chain</h2>
                    <div class="bg-slate-800 rounded px-3 py-1 flex items-center gap-2">
                        <span class="text-slate-400 text-xs font-bold">UNDERLYING:</span>
                        <span class="text-emerald-400 font-mono font-bold" id="oc-spot-price">---</span>
                    </div>
                </div>
                <button onclick="closeOptionChain()" class="text-slate-400 hover:text-white transition-colors"><i data-lucide="x" class="w-6 h-6"></i></button>
            </div>
            
            <!-- Tools -->
            <div class="bg-slate-50 border-b border-slate-200 p-3 flex items-center justify-between shrink-0">
                <div class="flex gap-2">
                    <select id="oc-symbol-select" onchange="loadOptionChain()" class="bg-white border border-slate-300 text-sm rounded px-3 py-1.5 font-bold outline-none focus:border-indigo-500 text-slate-700">
                        <option value="NIFTY50">NIFTY 50</option>
                        <option value="BANKNIFTY">BANK NIFTY</option>
                    </select>
                    <select class="bg-white border border-slate-300 text-sm rounded px-3 py-1.5 font-bold outline-none focus:border-indigo-500 text-slate-700">
                        <option>Current Expiry (Weekly)</option>
                    </select>
                </div>
                <div class="flex items-center gap-4 text-xs font-bold">
                    <span class="flex items-center gap-1 text-emerald-600"><div class="w-2 h-2 rounded-full bg-emerald-500"></div> ITM Calls</span>
                    <span class="flex items-center gap-1 text-rose-600"><div class="w-2 h-2 rounded-full bg-rose-500"></div> ITM Puts</span>
                </div>
            </div>
            
            <!-- Table Container -->
            <div class="flex-1 overflow-auto bg-slate-100 relative">
                <table class="w-full text-center text-xs whitespace-nowrap border-collapse">
                    <thead class="sticky top-0 z-10 bg-slate-800 text-slate-300 text-[10px] uppercase tracking-wider font-bold">
                        <tr>
                            <th colspan="4" class="py-2 border-b border-r border-slate-700">CALLS (CE)</th>
                            <th class="py-2 border-b border-slate-700 bg-slate-900 w-24">STRIKE</th>
                            <th colspan="4" class="py-2 border-b border-l border-slate-700">PUTS (PE)</th>
                        </tr>
                        <tr class="bg-slate-700 text-slate-200">
                            <th class="py-2 px-2 border-r border-slate-600">Action</th>
                            <th class="py-2 px-2 border-r border-slate-600">IV</th>
                            <th class="py-2 px-2 border-r border-slate-600">OI</th>
                            <th class="py-2 px-4 border-r border-slate-600 text-right text-emerald-400">LTP</th>
                            
                            <th class="py-2 px-4 bg-slate-900 text-white border-r border-l border-slate-800">PRICE</th>
                            
                            <th class="py-2 px-4 border-l border-slate-600 text-left text-rose-400">LTP</th>
                            <th class="py-2 px-2 border-l border-slate-600">OI</th>
                            <th class="py-2 px-2 border-l border-slate-600">IV</th>
                            <th class="py-2 px-2 border-l border-slate-600">Action</th>
                        </tr>
                    </thead>
                    <tbody id="oc-tbody" class="divide-y divide-slate-200 font-mono">
                        <!-- Filled by JS -->
                    </tbody>
                </table>
                <div id="oc-loader" class="absolute inset-0 bg-white/50 backdrop-blur-sm flex items-center justify-center hidden">
                    <div class="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            </div>
        </div>
    </div>
"""

content = content.replace("</body>", modal_html + "\n</body>")

# 3. Add JS for options
js_code = """
    /* --- OPTION CHAIN LOGIC --- */
    function openOptionChain() {
        document.getElementById('option-chain-modal').classList.remove('hidden');
        loadOptionChain();
    }
    
    function closeOptionChain() {
        document.getElementById('option-chain-modal').classList.add('hidden');
    }
    
    async function loadOptionChain() {
        const sym = document.getElementById('oc-symbol-select').value;
        const loader = document.getElementById('oc-loader');
        const tbody = document.getElementById('oc-tbody');
        
        loader.classList.remove('hidden');
        try {
            const res = await fetch(`/api/options/${sym}`);
            const data = await res.json();
            
            document.getElementById('oc-spot-price').innerText = data.spot.toFixed(2);
            
            tbody.innerHTML = '';
            
            data.chain.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-indigo-50/50 transition-colors bg-white';
                
                // ITM Highlighting logic
                const isCallITM = row.strike < data.spot;
                const isPutITM = row.strike > data.spot;
                
                const callBg = isCallITM ? 'bg-amber-50/30' : '';
                const putBg = isPutITM ? 'bg-amber-50/30' : '';
                
                tr.innerHTML = `
                    <td class="py-1 px-2 border-r border-slate-200 ${callBg}">
                        <div class="flex gap-1 justify-center">
                            <button onclick="prepareOptionTrade('${row.ce_symbol}', 'BUY', ${row.ce_price})" class="bg-emerald-100 text-emerald-700 hover:bg-emerald-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">B</button>
                            <button onclick="prepareOptionTrade('${row.ce_symbol}', 'SELL', ${row.ce_price})" class="bg-rose-100 text-rose-700 hover:bg-rose-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">S</button>
                        </div>
                    </td>
                    <td class="py-1 px-2 border-r border-slate-200 text-slate-500 ${callBg}">${row.ce_iv}%</td>
                    <td class="py-1 px-2 border-r border-slate-200 text-slate-600 ${callBg}">${(row.ce_oi/1000).toFixed(1)}k</td>
                    <td class="py-1 px-4 border-r border-slate-200 text-right font-bold text-emerald-600 ${callBg}">${row.ce_price.toFixed(2)}</td>
                    
                    <td class="py-2 px-4 bg-slate-50 font-black text-slate-800 border-x border-slate-300 text-sm shadow-inner">${row.strike}</td>
                    
                    <td class="py-1 px-4 border-l border-slate-200 text-left font-bold text-rose-600 ${putBg}">${row.pe_price.toFixed(2)}</td>
                    <td class="py-1 px-2 border-l border-slate-200 text-slate-600 ${putBg}">${(row.pe_oi/1000).toFixed(1)}k</td>
                    <td class="py-1 px-2 border-l border-slate-200 text-slate-500 ${putBg}">${row.pe_iv}%</td>
                    <td class="py-1 px-2 border-l border-slate-200 ${putBg}">
                        <div class="flex gap-1 justify-center">
                            <button onclick="prepareOptionTrade('${row.pe_symbol}', 'BUY', ${row.pe_price})" class="bg-emerald-100 text-emerald-700 hover:bg-emerald-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">B</button>
                            <button onclick="prepareOptionTrade('${row.pe_symbol}', 'SELL', ${row.pe_price})" class="bg-rose-100 text-rose-700 hover:bg-rose-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">S</button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            // Scroll to ATM
            setTimeout(() => {
                const rows = Array.from(tbody.children);
                const atmRow = rows[Math.floor(rows.length/2)];
                if(atmRow) atmRow.scrollIntoView({block: "center", behavior: "smooth"});
            }, 100);
            
        } catch(e) {
            console.error(e);
            showToast('Failed to load option chain.', 'error');
        } finally {
            loader.classList.add('hidden');
        }
    }
    
    function prepareOptionTrade(symbol, action, price) {
        closeOptionChain();
        document.getElementById('trade-symbol').innerText = symbol;
        // Optionally update the lot size input based on Nifty/Banknifty
        if (symbol.includes('BANK')) {
            document.getElementById('trade-lots').value = '15'; // BankNifty lot
        } else {
            document.getElementById('trade-lots').value = '25'; // Nifty lot
        }
        
        // Flash the quick trade panel to show where they should look
        const qt = document.querySelector('.bg-white.shadow-2xl');
        qt.classList.add('ring-4', 'ring-indigo-500', 'ring-opacity-50');
        setTimeout(() => qt.classList.remove('ring-4', 'ring-indigo-500', 'ring-opacity-50'), 1000);
        
        showToast(`Selected ${symbol} for ${action}. Setup lots in Quick Trade panel.`, 'success');
    }
"""

content = content.replace("</script>", js_code + "\n</script>")

with open('app/templates/trading_terminal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("INJECTED Option Chain HTML & JS")
'''

with open(TARGET, 'w') as f:
    f.write(script)

print("Created inject script")

