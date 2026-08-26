with open('scratch/write_terminal_ultimate.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will just replace the entire renderOptionChart function
pattern = r'    async function renderOptionChart\(symbol\) \{.*?catch\(e\) \{\}\s*\}'

replacement = """    async function renderOptionChart(symbol) {
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
            document.getElementById("lw_chart_container_1").innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#94a3b8;font-family:monospace;">Option Chart Loading Failed. Check CDN/Adblock.</div>';
        }
    }"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('scratch/write_terminal_ultimate.py', 'w', encoding='utf-8') as f:
    f.write(content)
