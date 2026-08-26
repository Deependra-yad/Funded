
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
                            <button onclick="prepareOptionTrade('${row.ce_symbol}', 'BUY')" class="bg-emerald-100 text-emerald-700 hover:bg-emerald-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">B</button>
                            <button onclick="prepareOptionTrade('${row.ce_symbol}', 'SELL')" class="bg-rose-100 text-rose-700 hover:bg-rose-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">S</button>
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
                            <button onclick="prepareOptionTrade('${row.pe_symbol}', 'BUY')" class="bg-emerald-100 text-emerald-700 hover:bg-emerald-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">B</button>
                            <button onclick="prepareOptionTrade('${row.pe_symbol}', 'SELL')" class="bg-rose-100 text-rose-700 hover:bg-rose-500 hover:text-white px-2 py-0.5 rounded text-[10px] font-bold transition-colors">S</button>
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
    


    var lwChart = null;
    var lwSeries = null;
    var lastLwCandle = null;

    async function renderOptionChart(symbol) {
        try {
            document.getElementById("tv_chart_container_1").style.display = "none";
            var lwContainer = document.getElementById("lw_chart_container_1");
            lwContainer.style.display = "block";
            lwContainer.innerHTML = "";
            
            // Allow DOM to reflow so clientWidth is populated
            await new Promise(r => setTimeout(r, 50));
            
            var w = lwContainer.clientWidth || 800;
            var h = lwContainer.clientHeight || 500;
            
            lwChart = LightweightCharts.createChart(lwContainer, {
                width: w,
                height: h,
                layout: { backgroundColor: '#ffffff', textColor: '#333' },
                grid: { vertLines: { color: '#f0f0f0' }, horzLines: { color: '#f0f0f0' } },
                timeScale: { timeVisible: true, secondsVisible: false },
            });
            
            lwSeries = lwChart.addCandlestickSeries({
                upColor: '#22c55e', downColor: '#ef4444', borderVisible: false,
                wickUpColor: '#22c55e', wickDownColor: '#ef4444'
            });

            var res = await fetch('/api/market/candles/' + symbol);
            var data = await res.json();
            var cData = data.map(c => ({
                time: c.time + 19800,
                open: c.open, high: c.high, low: c.low, close: c.close
            }));
            lwSeries.setData(cData);
            if(cData.length > 0) lastLwCandle = cData[cData.length - 1];
        } catch(e) {
            console.error("Option Chart Error:", e);
            document.getElementById("lw_chart_container_1").innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#94a3b8;font-family:monospace;">Option Chart Loading Failed: ' + e.message + ' <br> Stack: ' + e.stack + '</div>';
        }
    }

    function selectSymbol(sym) {
        var oldWl = document.getElementById('wl-' + activeSymbol);
        if(oldWl) oldWl.classList.remove('active');
        
        activeSymbol = sym;
        
        var newWl = document.getElementById('wl-' + activeSymbol);
        if(newWl) newWl.classList.add('active');
        
        document.getElementById('order-symbol-title').innerText = sym;
        
        if (sym.endsWith("CE") || sym.endsWith("PE")) {
            renderOptionChart(sym);
        } else {
            document.getElementById("lw_chart_container_1").style.display = "none";
            document.getElementById("tv_chart_container_1").style.display = "block";
            
            var tvSym = tvSymbolMap[sym] || ('BSE:' + sym);
            var interval = (tvSym.startsWith('BINGX') || tvSym.startsWith('BINANCE')) ? "5" : "D"; 
            
            document.getElementById("tv_chart_container_1").innerHTML = "";
            tvWidget1 = initTVWidget("tv_chart_container_1", tvSym, interval);
        }
    }

    function prepareOptionTrade(symbol, action) {
        closeOptionChain();
        selectSymbol(symbol); // Now actually select it so the chart changes!
        
        var qtyInput = document.getElementById('qt-qty');
        if (symbol.includes('BANK')) {
            qtyInput.value = '15';
        } else {
            qtyInput.value = '25';
        }
        
        placeTrade(action);
        showToast(`Placing ${action} order for ${symbol}...`, 'success');
    }

