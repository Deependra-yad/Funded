with open('scratch/write_terminal_ultimate.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Add Lightweight charts script tag
head_tag = r'    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>'
new_head = """    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>"""
content = content.replace(head_tag, new_head)

# Add lightweight chart container next to tv_chart_container_1
tv_container = r'<div id="tv_chart_container_1" class="w-full h-full relative"></div>'
new_container = """<div id="tv_chart_container_1" class="w-full h-full relative"></div>
                      <div id="lw_chart_container_1" class="w-full h-full relative hidden" style="position: absolute; top: 0; left: 0; z-index: 10; background: white;"></div>"""
content = content.replace(tv_container, new_container)

# Hide the BINGX message
bingx_msg = r'<div class="absolute bottom-4 right-4 bg-slate-800/80 text-white text-\[10px\] p-2 rounded backdrop-blur">\s*Using BINGX Crypto/Indices to bypass TV Intraday Blocks\.\s*</div>'
content = re.sub(bingx_msg, '', content)

# Remove the massive overlay because we will have actual charts now!
overlay_msg = r'<!-- DYNAMIC OPTION OVERLAY -->\s*<div id="chart-option-overlay" class="absolute top-4 left-4 z-50 pointer-events-none hidden">\s*<div class="bg-indigo-600/90 backdrop-blur text-white px-4 py-2 rounded-lg font-black text-xl shadow-\[0_0_15px_rgba\(79,70,229,0\.5\)\] border border-indigo-400">\s*<span id="chart-overlay-symbol"></span>\s*</div>\s*</div>'
content = re.sub(overlay_msg, '', content)

# Update Javascript
js_logic = """
    var lwChart = null;
    var lwSeries = null;
    var lastLwCandle = null;

    async function renderOptionChart(symbol) {
        document.getElementById("tv_chart_container_1").classList.add("hidden");
        var lwContainer = document.getElementById("lw_chart_container_1");
        lwContainer.classList.remove("hidden");
        lwContainer.innerHTML = "";
        
        lwChart = LightweightCharts.createChart(lwContainer, {
            width: lwContainer.clientWidth,
            height: lwContainer.clientHeight,
            layout: { backgroundColor: '#ffffff', textColor: '#333' },
            grid: { vertLines: { color: '#f0f0f0' }, horzLines: { color: '#f0f0f0' } },
            timeScale: { timeVisible: true, secondsVisible: false },
        });
        
        lwSeries = lwChart.addCandlestickSeries({
            upColor: '#22c55e', downColor: '#ef4444', borderVisible: false,
            wickUpColor: '#22c55e', wickDownColor: '#ef4444'
        });

        try {
            var res = await fetch('/api/market/candles/' + symbol);
            var data = await res.json();
            var cData = data.map(c => ({
                time: c.time + 19800, // IST timezone offset roughly
                open: c.open, high: c.high, low: c.low, close: c.close
            }));
            lwSeries.setData(cData);
            if(cData.length > 0) lastLwCandle = cData[cData.length - 1];
        } catch(e) {}
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
            document.getElementById("lw_chart_container_1").classList.add("hidden");
            document.getElementById("tv_chart_container_1").classList.remove("hidden");
            
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
"""

# Replace `selectSymbol` and `prepareOptionTrade` logic
content = re.sub(r'    function selectSymbol\(sym\) \{.*?\/\/ tv\.js widget doesn\'t support dynamic setSymbol, we must recreate the iframe.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'    function prepareOptionTrade\(symbol, action\) \{.*?showToast\(`Placing \$\{action\} order for \$\{symbol\}\.\.\.`, \'success\'\);\s*\}', '', content, flags=re.DOTALL)
# The previous regex might fail if it doesn't match perfectly, so let's just append the new logic inside the script tag

content = content.replace("</script>\n</body>", js_logic + "\n</script>\n</body>")

with open('scratch/write_terminal_ultimate.py', 'w', encoding='utf-8') as f:
    f.write(content)
