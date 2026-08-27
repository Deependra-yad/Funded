with open('app/routers/features.py', 'r', encoding='utf-8') as f:
    content = f.read()

detailed_features = """
FEATURE_CONTENT = {
    "heatmap": {
        "title": "Market Heatmap",
        "icon": "bar-chart",
        "desc": "Real-time visualization of market movers.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-crypto-coins-heatmap.js" async>{"dataSource": "Crypto","blockSize": "market_cap_calc","blockColor": "change","locale": "en","symbolUrl": "","colorTheme": "dark","hasTopBar": false,"isDataSetEnabled": false,"isZoomEnabled": true,"hasSymbolTooltip": true,"width": "100%","height": "100%"}</script></div>'''
    },
    "news": {
        "title": "Market News",
        "icon": "newspaper",
        "desc": "Latest fundamental news and economic updates.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>{"feedMode": "all_symbols","colorTheme": "dark","isTransparent": true,"displayMode": "regular","width": "100%","height": "100%","locale": "en"}</script></div>'''
    },
    "calendar": {
        "title": "Economic Calendar",
        "icon": "calendar",
        "desc": "Track key economic events and data releases.",
        "widget": '''<div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>{"colorTheme": "dark","isTransparent": true,"width": "100%","height": "100%","locale": "en","importanceFilter": "-1,0,1"}</script></div>'''
    },
    "leaderboard": {
        "title": "Leaderboard",
        "icon": "flag",
        "desc": "Top funded traders this month.",
        "widget": '''
        <div class="p-6">
            <div class="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4 flex items-center justify-between mb-6">
                <div>
                    <div class="text-indigo-400 font-bold">Your Global Rank</div>
                    <div class="text-2xl font-black text-white">#1,402</div>
                </div>
                <i data-lucide="award" class="w-10 h-10 text-indigo-500 opacity-50"></i>
            </div>
            <table class="w-full text-left">
                <thead><tr class="text-xs text-slate-500 uppercase"><th class="pb-3">Rank</th><th class="pb-3">Trader</th><th class="pb-3">Payout</th><th class="pb-3 text-right">Win Rate</th></tr></thead>
                <tbody class="text-slate-300">
                    <tr class="border-t border-slate-800"><td class="py-4 font-bold text-amber-500">1</td><td class="py-4 flex items-center gap-2"><img src="https://i.pravatar.cc/150?u=1" class="w-6 h-6 rounded-full"> Alex R.</td><td class="py-4 font-mono text-emerald-400">$142,500</td><td class="py-4 text-right">82%</td></tr>
                    <tr class="border-t border-slate-800"><td class="py-4 font-bold text-slate-300">2</td><td class="py-4 flex items-center gap-2"><img src="https://i.pravatar.cc/150?u=2" class="w-6 h-6 rounded-full"> Sarah M.</td><td class="py-4 font-mono text-emerald-400">$98,200</td><td class="py-4 text-right">79%</td></tr>
                    <tr class="border-t border-slate-800"><td class="py-4 font-bold text-amber-700">3</td><td class="py-4 flex items-center gap-2"><img src="https://i.pravatar.cc/150?u=3" class="w-6 h-6 rounded-full"> John D.</td><td class="py-4 font-mono text-emerald-400">$84,100</td><td class="py-4 text-right">76%</td></tr>
                </tbody>
            </table>
        </div>'''
    },
    "affiliate": {
        "title": "Affiliate Dashboard",
        "icon": "users",
        "desc": "Earn up to 20% commission on every referral.",
        "widget": '''
        <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-xs text-slate-400 uppercase">Total Earned</div>
                    <div class="text-2xl font-black text-emerald-400 mt-1">$0.00</div>
                </div>
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-xs text-slate-400 uppercase">Active Referrals</div>
                    <div class="text-2xl font-black text-white mt-1">0</div>
                </div>
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-xs text-slate-400 uppercase">Conversion Rate</div>
                    <div class="text-2xl font-black text-white mt-1">0%</div>
                </div>
            </div>
            <div class="mb-4 text-sm font-bold text-slate-400">Your Referral Link</div>
            <div class="flex gap-2">
                <input type="text" value="https://fundeddesk.com/ref/user123" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-slate-300" readonly>
                <button class="bg-primary text-white px-6 py-3 rounded-lg font-bold hover:bg-primary/80 transition-colors">Copy</button>
            </div>
        </div>'''
    },
    "support": {
        "title": "Help & Support",
        "icon": "life-buoy",
        "desc": "24/7 Priority Support for all our traders.",
        "widget": '''
        <div class="p-6 text-center max-w-lg mx-auto py-12">
            <div class="w-20 h-20 bg-blue-500/10 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <i data-lucide="message-square" class="w-10 h-10"></i>
            </div>
            <h3 class="text-xl font-bold text-white mb-2">Live Chat Support</h3>
            <p class="text-slate-400 mb-8">Our average response time is under 3 minutes. Connect with a risk management specialist instantly.</p>
            <button class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-8 rounded-xl w-full transition-colors">Start Conversation</button>
            <div class="mt-6 text-sm text-slate-500">Alternatively, email us at support@fundeddesk.com</div>
        </div>'''
    },
    "coupons": {
        "title": "Coupon Codes",
        "icon": "ticket",
        "desc": "Exclusive discounts and active promotions.",
        "widget": '''
        <div class="p-6 space-y-4">
            <div class="bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-500/30 p-6 rounded-2xl flex justify-between items-center">
                <div>
                    <div class="text-amber-500 font-black text-xl mb-1">SUMMER20</div>
                    <div class="text-slate-300 text-sm">Get 20% off all 1-Step Evaluation accounts. Valid until Aug 31.</div>
                </div>
                <button class="bg-amber-600 text-white font-bold py-2 px-6 rounded-lg shadow-lg hover:bg-amber-500">Copy</button>
            </div>
            <div class="bg-slate-800/50 border border-slate-700 p-6 rounded-2xl flex justify-between items-center">
                <div>
                    <div class="text-white font-black text-xl mb-1">RETRY10</div>
                    <div class="text-slate-400 text-sm">10% discount on challenge retries. Always active.</div>
                </div>
                <button class="bg-slate-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-slate-600">Copy</button>
            </div>
        </div>'''
    },
    "giveaway": {
        "title": "FundedFirm Giveaway",
        "icon": "gift",
        "desc": "Participate to win free funded accounts.",
        "widget": '''
        <div class="p-6 text-center max-w-lg mx-auto py-12">
            <h2 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">Win a $100k Account</h2>
            <p class="text-slate-400 mb-8">Join our monthly giveaway. Complete social tasks to earn entries!</p>
            <div class="grid grid-cols-3 gap-4 mb-8">
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-2xl font-black text-white">12</div>
                    <div class="text-[10px] text-slate-500 uppercase mt-1">Days</div>
                </div>
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-2xl font-black text-white">08</div>
                    <div class="text-[10px] text-slate-500 uppercase mt-1">Hours</div>
                </div>
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <div class="text-2xl font-black text-white">45</div>
                    <div class="text-[10px] text-slate-500 uppercase mt-1">Mins</div>
                </div>
            </div>
            <button class="bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 px-8 rounded-xl w-full shadow-lg shadow-pink-500/20 hover:scale-105 transition-transform">Enter Giveaway Now</button>
        </div>'''
    },
    "comparison": {
        "title": "Account Comparison",
        "icon": "arrow-left-right",
        "desc": "Compare evaluation models side by side.",
        "widget": '''
        <div class="p-6 overflow-x-auto">
            <table class="w-full text-left">
                <thead><tr class="text-xs text-slate-400 uppercase bg-slate-800/50"><th class="p-4">Feature</th><th class="p-4">1-Step</th><th class="p-4">2-Step</th><th class="p-4">Instant</th></tr></thead>
                <tbody class="text-slate-300 divide-y divide-slate-800">
                    <tr><td class="p-4 font-bold text-white">Profit Target</td><td class="p-4 text-emerald-400 font-mono">10%</td><td class="p-4 text-emerald-400 font-mono">8% / 5%</td><td class="p-4 text-emerald-400 font-mono">10%</td></tr>
                    <tr><td class="p-4 font-bold text-white">Max Daily Loss</td><td class="p-4 text-rose-400 font-mono">4%</td><td class="p-4 text-rose-400 font-mono">5%</td><td class="p-4 text-rose-400 font-mono">5%</td></tr>
                    <tr><td class="p-4 font-bold text-white">Max Total Loss</td><td class="p-4 text-rose-400 font-mono">6%</td><td class="p-4 text-rose-400 font-mono">10%</td><td class="p-4 text-rose-400 font-mono">10%</td></tr>
                    <tr><td class="p-4 font-bold text-white">Time Limit</td><td class="p-4">Infinite</td><td class="p-4">Infinite</td><td class="p-4">Infinite</td></tr>
                    <tr><td class="p-4 font-bold text-white">Profit Split</td><td class="p-4 font-mono">80% - 90%</td><td class="p-4 font-mono">80% - 90%</td><td class="p-4 font-mono">70%</td></tr>
                </tbody>
            </table>
        </div>'''
    },
    "rules": {
        "title": "Trading Rules",
        "icon": "clipboard-list",
        "desc": "Core guidelines to keep your account safe.",
        "widget": '''
        <div class="p-6 space-y-6 text-slate-300">
            <div>
                <h4 class="text-white font-bold mb-2 flex items-center gap-2"><i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500"></i> Expert Advisors (EAs)</h4>
                <p class="text-sm text-slate-400">You are fully allowed to use EAs, provided they do not use latency arbitrage or high-frequency tick scalping.</p>
            </div>
            <div>
                <h4 class="text-white font-bold mb-2 flex items-center gap-2"><i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500"></i> News Trading</h4>
                <p class="text-sm text-slate-400">Trading during high-impact news is permitted on all accounts. However, slippage is out of our control.</p>
            </div>
            <div>
                <h4 class="text-white font-bold mb-2 flex items-center gap-2"><i data-lucide="alert-triangle" class="w-4 h-4 text-rose-500"></i> Account Sharing</h4>
                <p class="text-sm text-slate-400">Accessing your account from different countries simultaneously or sharing credentials will result in instant termination.</p>
            </div>
        </div>'''
    },
    "privacy": {
        "title": "Data & Privacy",
        "icon": "lock",
        "desc": "Manage how we handle your personal data.",
        "widget": '''
        <div class="p-6 max-w-2xl">
            <p class="text-slate-400 mb-6">We take your privacy seriously. Your KYC documents and trading data are encrypted using bank-grade AES-256 encryption.</p>
            <div class="space-y-4">
                <label class="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700 cursor-pointer">
                    <input type="checkbox" checked class="w-5 h-5 accent-emerald-500">
                    <div>
                        <div class="font-bold text-white">Marketing Emails</div>
                        <div class="text-xs text-slate-400">Receive updates about new features and discounts.</div>
                    </div>
                </label>
                <label class="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700 cursor-pointer">
                    <input type="checkbox" checked class="w-5 h-5 accent-emerald-500">
                    <div>
                        <div class="font-bold text-white">Performance Analytics</div>
                        <div class="text-xs text-slate-400">Allow us to anonymously aggregate your trading data for public statistics.</div>
                    </div>
                </label>
            </div>
        </div>'''
    }
}
"""

import re
content = re.sub(r'FEATURE_CONTENT\s*=\s*\{.*?\n}', detailed_features, content, flags=re.DOTALL)

with open('app/routers/features.py', 'w', encoding='utf-8') as f:
    f.write(content)

