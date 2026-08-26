
    lucide.createIcons();

    // STATE
    var activeSymbol = document.body.getAttribute('data-active-symbol') || 'NIFTY50';
    var accAttr = document.body.getAttribute('data-account-id');
    var activeAccountId = (accAttr && accAttr !== 'null' && accAttr !== 'None') ? parseInt(accAttr) : null;
    
    var tvWidget1 = null;
    var tvWidget2 = null;
    var isDualChart = false;
    var isTrading = false;
    var pricesData = {};

    // TRADINGVIEW SYMBOL FIX (Intraday Compatible)
    // TradingView entirely blocks intraday (1m, 5m) on ALL Indian Exchanges (NSE/BSE) on free widgets.
    // We strictly use BINGX Perpetuals (which track NIFTY flawlessly 24/7 and allow 1m/5m charting).
    var tvSymbolMap = {
        'NIFTY50': 'BINGX:NIFTY50USDT.P', 
        'BANKNIFTY': 'BINGX:BTCUSDT', // BINGX doesn't have BankNifty, using BTC as fallback to ensure chart always loads
        'SENSEX': 'BSE:SENSEX',       // Daily only
        'FINNIFTY': 'BINGX:ETHUSDT',  // Fallback
        'MIDCPNIFTY': 'BINGX:SOLUSDT', // Fallback
        'RELIANCE': 'BSE:RELIANCE',   // Daily only
        'HDFCBANK': 'BSE:HDFCBANK'
    };

    function formatInr(val) {
        if(!val || isNaN(val)) return "0.00";
        return val.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    }

    function showToast(message, type) {
        var container = document.getElementById('toast-container');
        var toast = document.createElement('div');
        toast.className = 'toast ' + (type || 'success');
        toast.innerText = message;
        container.appendChild(toast);
        setTimeout(() => { toast.style.animation = 'slideOut 0.3s ease forwards'; setTimeout(() => toast.remove(), 300); }, 3000);
    }

    function initTVWidget(containerId, sym, interval) {
        return new TradingView.widget({
            "autosize": true,
            "symbol": sym,
            "interval": interval,
            "timezone": "Asia/Kolkata",
            "theme": "light",
            "style": "1",
            "locale": "in",
            "enable_publishing": false,
            "backgroundColor": "#ffffff",
            "gridColor": "#f1f5f9",
            "hide_top_toolbar": false,
            "hide_side_toolbar": false,
            "hide_legend": true,
            "save_image": false,
            "container_id": containerId,
            "toolbar_bg": "#ffffff",
            "allow_symbol_change": false,
            "disabled_features": ["header_symbol_search", "header_compare"],
            "studies": ["Volume@tv-basicstudies"]
        });
    }

    function initCharts() {
        var tvSym = tvSymbolMap[activeSymbol] || ('BSE:' + activeSymbol);
        var interval = (tvSym.startsWith('BINGX') || tvSym.startsWith('BINANCE')) ? "5" : "D"; 
        tvWidget1 = initTVWidget("tv_chart_container_1", tvSym, interval);
        
        // Ensure active symbol is highlighted in watchlist
        var wl = document.getElementById('wl-' + activeSymbol);
        if(wl) wl.classList.add('active');
    }

    function toggleDualChart() {
        var wrapper2 = document.getElementById('right-chart-wrapper');
        isDualChart = !isDualChart;
        
        if (isDualChart) {
            wrapper2.classList.remove('hidden');
            if (!tvWidget2) {
                // Initialize second chart to BankNifty equivalent
                var tvSym2 = tvSymbolMap['BANKNIFTY'];
                var interval = (tvSym2.startsWith('BINGX') || tvSym2.startsWith('BINANCE')) ? "5" : "D";
                tvWidget2 = initTVWidget("tv_chart_container_2", tvSym2, interval);
            }
        } else {
            wrapper2.classList.add('hidden');
        }
    }

    function toggleFullscreen() {
        var elem = document.getElementById("dual-chart-container");
        if (!document.fullscreenElement) {
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) { /* Safari */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { /* IE11 */
                document.msExitFullscreen();
            }
        }
    }




    async function pollPrices() {
        try {
            var res = await fetch('/api/market/prices?active_symbol=' + activeSymbol);
            var prices = await res.json();
            
            for(var i = 0; i < prices.length; i++) {
                var p = prices[i];
                pricesData[p.symbol] = p;
                
                var wlBid = document.getElementById('wl-bid-' + p.symbol);
                var wlAsk = document.getElementById('wl-ask-' + p.symbol);
                if(wlBid) wlBid.innerText = p.bid.toFixed(2);
                if(wlAsk) wlAsk.innerText = p.ask.toFixed(2);

                if(p.symbol === activeSymbol) {
                    var qtBid = document.getElementById('qt-bid');
                    var qtAsk = document.getElementById('qt-ask');
                    if(qtBid) qtBid.innerText = p.bid.toFixed(2);
                    if(qtAsk) qtAsk.innerText = p.ask.toFixed(2);
                    
                    if (typeof lwSeries !== 'undefined' && lwSeries && lastLwCandle && (activeSymbol.endsWith("CE") || activeSymbol.endsWith("PE"))) {
                        var now = Math.floor(Date.now() / 1000) + 19800; // IST rough
                        if (now - lastLwCandle.time > 300) {
                            lastLwCandle = {time: now, open: p.mid, high: p.mid, low: p.mid, close: p.mid};
                        } else {
                            lastLwCandle.close = p.mid;
                            lastLwCandle.high = Math.max(lastLwCandle.high, p.mid);
                            lastLwCandle.low = Math.min(lastLwCandle.low, p.mid);
                        }
                        lwSeries.update(lastLwCandle);
                    }
                }
            }
        } catch (e) {}
    }

    async function pollAccountState() {
        if (!activeAccountId) return;
        try {
            var url = '/api/account/' + activeAccountId + '/state';
            var res = await fetch(url);
            var data = await res.json();
            var st = data.state;

            document.getElementById('top-balance').innerText = '\u20B9' + formatInr(st.balance);
            document.getElementById('top-equity').innerText = '\u20B9' + formatInr(st.equity);
            
            var pnlVal = st.floating_pnl || 0;
            var pnlColor = pnlVal >= 0 ? 'text-emerald-500' : 'text-rose-500';
            var pnlSign = pnlVal >= 0 ? '+\u20B9' : '-\u20B9';
            document.getElementById('top-pnl').innerHTML = '<span class="' + pnlColor + '">' + pnlSign + formatInr(Math.abs(pnlVal)) + '</span>';

            var tbody = document.getElementById('pos-tbody');
            var posCount = data.positions ? data.positions.length : 0;
            document.getElementById('pos-count').innerText = posCount;
            
            var html = '';
            if(posCount > 0) {
                for(var i = 0; i < data.positions.length; i++) {
                    var pos = data.positions[i];
                    var isBuy = pos.order_type === 'BUY';
                    var pC = pos.pnl >= 0 ? 'text-emerald-600' : 'text-rose-600';
                    var pS = pos.pnl >= 0 ? '+\u20B9' : '-\u20B9';
                    html += '<tr class="hover:bg-slate-50">';
                    html += '<td class="py-2.5 px-4 font-semibold text-slate-500">' + pos.ticket + '</td>';
                    html += '<td class="py-2.5 px-4 font-bold text-slate-900">' + pos.symbol + '</td>';
                    html += '<td class="py-2.5 px-4 font-black ' + (isBuy ? 'text-emerald-600' : 'text-rose-600') + '">' + pos.order_type + '</td>';
                    html += '<td class="py-2.5 px-4 text-slate-800">' + pos.volume_lots + '</td>';
                    html += '<td class="py-2.5 px-4 text-slate-800">' + pos.open_price + '</td>';
                    html += '<td class="py-2.5 px-4 font-bold text-slate-900">' + pos.current_price + '</td>';
                    html += '<td class="py-2.5 px-4 text-slate-400">-</td>';
                    html += '<td class="py-2.5 px-4 text-right font-black ' + pC + '">' + pS + formatInr(Math.abs(pos.pnl)) + '</td>';
                    html += '<td class="py-2.5 px-4 text-center"><button onclick="closeTrade(' + pos.id + ')" class="text-[10px] font-bold uppercase tracking-wider bg-rose-50 text-rose-600 border border-rose-200 px-3 py-1 rounded hover:bg-rose-500 hover:text-white transition-colors">Close</button></td>';
                    html += '</tr>';
                }
            } else {
                html = '<tr><td colspan="9" class="text-center py-8 text-slate-400 font-sans text-xs">No open positions</td></tr>';
            }
            tbody.innerHTML = html;
            
            if(data.notifications && data.notifications.length > 0) {
                for(var i=0; i < data.notifications.length; i++) {
                    showToast('LIVEMESSAGE: ' + data.notifications[i], 'success');
                }
            }
        } catch (e) { console.error(e); }
    }

    async function placeTrade(orderType) {
        if(isTrading) return;
        var qtyInput = document.getElementById('qt-qty');
        var lots = parseFloat(qtyInput.value);
        if (!lots || lots <= 0) return showToast('Invalid volume', 'error');

        isTrading = true;
        var formData = new FormData();
        formData.append('account_id', activeAccountId);
        formData.append('symbol', activeSymbol);
        formData.append('order_type', orderType);
        formData.append('volume_lots', lots);

        try {
            var res = await fetch('/api/trade/open', { method: 'POST', body: formData });
            var data = await res.json();
            if (data.success) {
                showToast('Filled: ' + orderType + ' ' + lots + ' ' + activeSymbol, 'success');
                pollAccountState();
            } else {
                showToast(data.error || 'Trade rejected', 'error');
            }
        } catch (err) { showToast('Network error', 'error'); } finally { isTrading = false; }
    }

    async function closeTrade(tradeId) {
        try {
            var url = '/api/trade/close/' + tradeId;
            var res = await fetch(url, { method: 'POST' });
            var data = await res.json();
            if (data.success) { showToast('Position closed', 'success'); pollAccountState(); }
        } catch (err) {}
    }

    function switchTab(tab) {
        if(tab === 'positions') {
            document.getElementById('view-pos').classList.remove('hidden');
            document.getElementById('view-hist').classList.add('hidden');
        } else {
            document.getElementById('view-pos').classList.add('hidden');
            document.getElementById('view-hist').classList.remove('hidden');
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        initCharts();
        pollPrices();
        pollAccountState();
        setInterval(pollPrices, 1000);
        setInterval(pollAccountState, 1000);
    });
