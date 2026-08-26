import re

with open('app/templates/trading_terminal.html', 'r', encoding='utf-8') as f:
    html = f.read()

search_div = '''
              <div class="px-4 py-2 bg-slate-50 border-b border-slate-200">
                  <div class="relative">
                      <i data-lucide="search" class="w-4 h-4 absolute left-3 top-2.5 text-slate-400"></i>
                      <input type="text" id="symbol-search" placeholder="Search strikes (e.g. NIFTY24000CE)..." class="w-full bg-white border border-slate-300 rounded pl-9 pr-3 py-1.5 text-xs font-bold text-slate-700 outline-none focus:border-indigo-500 uppercase" autocomplete="off">
                      <!-- Search Results Dropdown -->
                      <div id="search-results" class="absolute left-0 right-0 top-9 bg-white border border-slate-200 rounded-b shadow-lg z-50 hidden max-h-60 overflow-y-auto"></div>
                  </div>
              </div>
'''

html = re.sub(r'<div class="px-4 py-2 bg-slate-50 border-b border-slate-200">\s*<div class="relative">[\s\S]*?</div>\s*</div>', search_div, html)

js_logic = '''
    const searchInput = document.getElementById('symbol-search');
    const searchResults = document.getElementById('search-results');

    const baseInstruments = ['NIFTY50', 'BANKNIFTY', 'SENSEX', 'CRUDEOIL', 'GOLD', 'EURUSD', 'BTCUSD'];

    searchInput.addEventListener('input', function(e) {
        const query = this.value.toUpperCase().replace(/\s+/g, '');
        if (query.length < 2) {
            searchResults.classList.add('hidden');
            return;
        }

        let suggestions = [];

        baseInstruments.forEach(inst => {
            if (inst.includes(query)) suggestions.push(inst);
        });

        const optMatch = query.match(/^([A-Z]+)(\d{2,})?(C|P|CE|PE)?$/);
        if (optMatch) {
            const base = optMatch[1];
            const strikePart = optMatch[2] || '';
            
            if (['NIFTY', 'BANKNIFTY', 'SENSEX'].includes(base)) {
                let strikeBase = 24000;
                let step = 50;
                if (base === 'BANKNIFTY') { strikeBase = 52000; step = 100; }
                if (base === 'SENSEX') { strikeBase = 80000; step = 100; }

                if (strikePart.length >= 2) {
                    const targetStr = strikePart.padEnd(5, '0');
                    const targetVal = parseInt(targetStr);
                    const nearest = Math.round(targetVal / step) * step;
                    
                    for (let i = -3; i <= 3; i++) {
                        const s = nearest + (i * step);
                        suggestions.push(`${base}${s}CE`);
                        suggestions.push(`${base}${s}PE`);
                    }
                } else if (strikePart.length === 0) {
                    for (let i = -2; i <= 2; i++) {
                        const s = strikeBase + (i * step);
                        suggestions.push(`${base}${s}CE`);
                        suggestions.push(`${base}${s}PE`);
                    }
                }
            }
        }

        suggestions = suggestions.filter(s => s.includes(query));
        suggestions = [...new Set(suggestions)].slice(0, 10);

        if (suggestions.length > 0) {
            searchResults.innerHTML = suggestions.map(sym => 
                `<div class="px-4 py-2 text-xs font-bold text-slate-700 hover:bg-indigo-50 hover:text-indigo-700 cursor-pointer border-b border-slate-50 last:border-0" 
                      onclick="addSymbolToWatchlist('${sym}'); selectSymbol('${sym}'); document.getElementById('search-results').classList.add('hidden'); document.getElementById('symbol-search').value='';">
                    ${sym}
                </div>`
            ).join('');
            searchResults.classList.remove('hidden');
        } else {
            searchResults.classList.add('hidden');
        }
    });

    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            var sym = this.value.toUpperCase().replace(/\s+/g, '');
            if (sym) {
                addSymbolToWatchlist(sym);
                selectSymbol(sym);
                this.value = '';
                searchResults.classList.add('hidden');
            }
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.add('hidden');
        }
    });
'''

html = re.sub(r'document\.getElementById\(\'symbol-search\'\)\.addEventListener\(\'keypress\', function\(e\) \{[\s\S]*?\}\);', js_logic, html)

with open('app/templates/trading_terminal.html', 'w', encoding='utf-8') as f:
    f.write(html)

