import random
import time
import threading
import httpx
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any

# Institutional Market Instruments
INSTRUMENTS = {
    "NIFTY50": {
        "name": "NIFTY 50 Index (NSE)",
        "category": "Indices",
        "base_price": 24200.0,
        "spread": 1.5,
        "digits": 2,
        "pip_size": 1.0,
        "contract_size": 25,  # Lot size for Nifty
        "volatility": 1.5,
    },
    "BANKNIFTY": {
        "name": "NIFTY BANK Index (NSE)",
        "category": "Indices",
        "base_price": 57500.0,
        "spread": 2.5,
        "digits": 2,
        "pip_size": 1.0,
        "contract_size": 15,  # Lot size for BankNifty
        "volatility": 3.0,
    },
    "SENSEX": {
        "name": "BSE SENSEX Index",
        "category": "Indices",
        "base_price": 80500.0,
        "spread": 5.0,
        "digits": 2,
        "pip_size": 1.0,
        "contract_size": 10,
        "volatility": 4.0,
    },
    "FINNIFTY": {
        "name": "NIFTY FIN SERVICE (NSE)",
        "category": "Indices",
        "base_price": 22500.0,
        "spread": 1.2,
        "digits": 2,
        "pip_size": 1.0,
        "contract_size": 25,
        "volatility": 1.2,
    },
    "MIDCPNIFTY": {
        "name": "NIFTY MIDCAP SELECT",
        "category": "Indices",
        "base_price": 12500.0,
        "spread": 1.0,
        "digits": 2,
        "pip_size": 1.0,
        "contract_size": 50,
        "volatility": 1.0,
    },
    "RELIANCE": {
        "name": "Reliance Industries (NSE)",
        "category": "Equities",
        "base_price": 2950.0,
        "spread": 0.5,
        "digits": 2,
        "pip_size": 0.05,
        "contract_size": 250,
        "volatility": 0.5,
    },
    "HDFCBANK": {
        "name": "HDFC Bank Ltd (NSE)",
        "category": "Equities",
        "base_price": 1650.0,
        "spread": 0.3,
        "digits": 2,
        "pip_size": 0.05,
        "contract_size": 550,
        "volatility": 10.0,
    }
}

class MarketDataEngine:
    def __init__(self):
        self.prices: Dict[str, Dict[str, float]] = {}
        self.candle_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.lock = threading.Lock()
        self._initialize_prices()
        self._sync_live_crypto()

    def _initialize_prices(self):
        for symbol, cfg in INSTRUMENTS.items():
            mid = cfg["base_price"]
            spread = cfg["spread"]
            self.prices[symbol] = {
                "bid": round(mid - spread / 2, cfg["digits"]),
                "ask": round(mid + spread / 2, cfg["digits"]),
                "mid": mid,
                "change_24h": round(random.uniform(-1.2, 2.5), 2),
                "high_24h": round(mid * 1.018, cfg["digits"]),
                "low_24h": round(mid * 0.982, cfg["digits"]),
            }
            self.candle_cache[symbol] = self._generate_initial_candles(symbol, count=120)

    def _sync_live_crypto(self):
        """Fetch live crypto market prices in background thread if internet is connected"""
        def fetch_worker():
            try:
                with httpx.Client(timeout=3.0) as client:
                    res = client.get("https://api.binance.com/api/v3/ticker/24hr")
                    if res.status_code == 200:
                        data = res.json()
                        crypto_map = {"BTCUSDT": "BTCUSD", "ETHUSDT": "ETHUSD", "SOLUSDT": "SOLUSD"}
                        with self.lock:
                            for item in data:
                                sym = item.get("symbol")
                                if sym in crypto_map:
                                    target_sym = crypto_map[sym]
                                    last_p = float(item.get("lastPrice", 0))
                                    change = float(item.get("priceChangePercent", 0))
                                    high = float(item.get("highPrice", 0))
                                    low = float(item.get("lowPrice", 0))
                                    if last_p > 0 and target_sym in self.prices:
                                        cfg = INSTRUMENTS[target_sym]
                                        self.prices[target_sym]["mid"] = round(last_p, cfg["digits"])
                                        self.prices[target_sym]["bid"] = round(last_p - cfg["spread"] / 2, cfg["digits"])
                                        self.prices[target_sym]["ask"] = round(last_p + cfg["spread"] / 2, cfg["digits"])
                                        self.prices[target_sym]["change_24h"] = round(change, 2)
                                        self.prices[target_sym]["high_24h"] = round(high, cfg["digits"])
                                        self.prices[target_sym]["low_24h"] = round(low, cfg["digits"])
            except Exception:
                pass # Silently proceed with local stochastic generation if offline

        t = threading.Thread(target=fetch_worker, daemon=True)
        t.start()

    def _generate_initial_candles(self, symbol: str, count: int = 120) -> List[Dict[str, Any]]:
        cfg = INSTRUMENTS[symbol]
        candles = []
        now = datetime.now(timezone.utc)
        current_p = cfg["base_price"]

        for i in range(count, 0, -1):
            t = now - timedelta(minutes=i * 5)
            timestamp = int(t.timestamp())
            
            vol = cfg["volatility"] * random.uniform(0.6, 1.8)
            drift = random.uniform(-vol, vol)
            open_p = current_p
            close_p = open_p + drift
            high_p = max(open_p, close_p) + abs(random.uniform(0, vol * 1.1))
            low_p = min(open_p, close_p) - abs(random.uniform(0, vol * 1.1))
            
            candles.append({
                "time": timestamp,
                "open": round(open_p, cfg["digits"]),
                "high": round(high_p, cfg["digits"]),
                "low": round(low_p, cfg["digits"]),
                "close": round(close_p, cfg["digits"]),
                "volume": int(random.uniform(150, 4500))
            })
            current_p = close_p

        self.prices[symbol]["mid"] = round(current_p, cfg["digits"])
        self.prices[symbol]["bid"] = round(current_p - cfg["spread"] / 2, cfg["digits"])
        self.prices[symbol]["ask"] = round(current_p + cfg["spread"] / 2, cfg["digits"])
        return candles

    def tick(self, symbol: str = None) -> Dict[str, Any]:
        """Advance price ticks dynamically"""
        symbols_to_tick = [symbol] if symbol and symbol in INSTRUMENTS else list(INSTRUMENTS.keys())
        updated = {}

        with self.lock:
            for sym in symbols_to_tick:
                cfg = INSTRUMENTS[sym]
                cur_mid = self.prices[sym]["mid"]
                vol = cfg["volatility"] * random.uniform(0.4, 1.6)
                step = random.gauss(0, vol)
                
                new_mid = max(cfg["base_price"] * 0.4, cur_mid + step)
                new_bid = round(new_mid - cfg["spread"] / 2, cfg["digits"])
                new_ask = round(new_mid + cfg["spread"] / 2, cfg["digits"])
                
                self.prices[sym]["mid"] = round(new_mid, cfg["digits"])
                self.prices[sym]["bid"] = new_bid
                self.prices[sym]["ask"] = new_ask

                if sym in self.candle_cache and self.candle_cache[sym]:
                    last_c = self.candle_cache[sym][-1]
                    now_ts = int(time.time())
                    if now_ts - last_c["time"] < 300:
                        last_c["close"] = round(new_mid, cfg["digits"])
                        last_c["high"] = max(last_c["high"], round(new_mid, cfg["digits"]))
                        last_c["low"] = min(last_c["low"], round(new_mid, cfg["digits"]))
                        last_c["volume"] += 1
                    else:
                        self.candle_cache[sym].append({
                            "time": now_ts,
                            "open": round(new_mid, cfg["digits"]),
                            "high": round(new_mid, cfg["digits"]),
                            "low": round(new_mid, cfg["digits"]),
                            "close": round(new_mid, cfg["digits"]),
                            "volume": 1
                        })
                        if len(self.candle_cache[sym]) > 500:
                            self.candle_cache[sym].pop(0)

                updated[sym] = {
                    "symbol": sym,
                    "name": cfg["name"],
                    "category": cfg["category"],
                    "bid": new_bid,
                    "ask": new_ask,
                    "mid": round(new_mid, cfg["digits"]),
                    "spread_pips": round(cfg["spread"] / cfg["pip_size"], 1),
                    "digits": cfg["digits"],
                    "change_24h": self.prices[sym]["change_24h"]
                }

        return updated

    def get_all_prices(self) -> List[Dict[str, Any]]:
        self.tick()
        with self.lock:
            result = []
            for sym, cfg in INSTRUMENTS.items():
                p = self.prices[sym]
                result.append({
                    "symbol": sym,
                    "name": cfg["name"],
                    "category": cfg["category"],
                    "bid": p["bid"],
                    "ask": p["ask"],
                    "mid": p["mid"],
                    "spread_pips": round(cfg["spread"] / cfg["pip_size"], 1),
                    "digits": cfg["digits"],
                    "change_24h": p["change_24h"],
                    "high_24h": p["high_24h"],
                    "low_24h": p["low_24h"]
                })
            return result

    def get_candles(self, symbol: str) -> List[Dict[str, Any]]:
        with self.lock:
            if symbol not in self.candle_cache:
                self.candle_cache[symbol] = self._generate_initial_candles(symbol)
            return list(self.candle_cache[symbol])

    def calculate_pnl(self, symbol: str, order_type: str, lots: float, open_price: float) -> tuple[float, float, float]:
        if symbol not in INSTRUMENTS:
            return 0.0, open_price, 0.0
        
        cfg = INSTRUMENTS[symbol]
        cur_p = self.prices[symbol]
        
        if order_type == "BUY":
            current_exit_price = cur_p["bid"]
            diff = current_exit_price - open_price
        else:
            current_exit_price = cur_p["ask"]
            diff = open_price - current_exit_price

        pips = diff / cfg["pip_size"]
        pnl = diff * lots * cfg["contract_size"]
        
        # Indian Market Simulated Fees (STT + Exchange Transaction Charges + Brokerage)
        turnover = (open_price + current_exit_price) * lots * cfg["contract_size"]
        stt_and_charges = turnover * 0.000125  # 0.0125% combined friction
        brokerage = 40.0  # ₹40 round trip per simulated trade
        total_fees = stt_and_charges + brokerage
        
        pnl -= total_fees

        if "JPY" in symbol:
            pnl = pnl / cur_p["mid"]

        return round(pnl, 2), round(current_exit_price, cfg["digits"]), round(pips, 1)

# Global engine instance
market_engine = MarketDataEngine()
