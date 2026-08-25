import math
from datetime import datetime, timedelta

def norm_cdf(x):
    """Cumulative distribution function for the standard normal distribution."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def black_scholes(S, K, T, r, sigma, option_type='CE'):
    """
    S: Spot price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free rate
    sigma: Volatility
    """
    if T <= 0:
        if option_type == 'CE': return max(0.0, S - K)
        else: return max(0.0, K - S)
        
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'CE':
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    else:
        return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def generate_option_chain(symbol, current_spot, strike_step=50, num_strikes=10, dte=3, volatility=0.15):
    """Generates a realistic mock option chain for a given underlying."""
    atm_strike = round(current_spot / strike_step) * strike_step
    
    chain = []
    T = dte / 365.0  # Time to expiry in years
    r = 0.05  # Risk free rate (5%)
    
    for i in range(-num_strikes, num_strikes + 1):
        strike = atm_strike + (i * strike_step)
        
        # Volatility skew simulation
        skew = -0.0001 * (strike - atm_strike)
        current_vol = max(0.05, volatility + skew)
        
        ce_price = black_scholes(current_spot, strike, T, r, current_vol, 'CE')
        pe_price = black_scholes(current_spot, strike, T, r, current_vol, 'PE')
        
        chain.append({
            "strike": strike,
            "ce_symbol": f"{symbol}{strike}CE",
            "pe_symbol": f"{symbol}{strike}PE",
            "ce_price": round(ce_price, 2),
            "pe_price": round(pe_price, 2),
            "ce_oi": int(abs(ce_price * 1000) % 500000 + 10000), 
            "pe_oi": int(abs(pe_price * 1000) % 500000 + 10000),
            "ce_iv": round(current_vol * 100, 1), 
            "pe_iv": round(current_vol * 100, 1)
        })
        
    return chain

def calculate_option_price_live(option_symbol, underlying_spot):
    """
    Given a symbol like NIFTY24200CE and the live NIFTY spot price, 
    calculates its live price on the fly.
    """
    if option_symbol.endswith('CE') or option_symbol.endswith('PE'):
        try:
            # Parse NIFTY24200CE -> underlying=NIFTY, strike=24200, type=CE
            opt_type = option_symbol[-2:]
            
            # Simple parsing: find the first digit
            digit_start = -1
            for i, char in enumerate(option_symbol):
                if char.isdigit():
                    digit_start = i
                    break
                    
            if digit_start != -1:
                underlying = option_symbol[:digit_start]
                strike_str = option_symbol[digit_start:-2]
                strike = float(strike_str)
                
                # We use fixed DTE and Volatility for the live price simulation
                T = 3 / 365.0
                r = 0.05
                vol = 0.15 - 0.0001 * (strike - underlying_spot)
                vol = max(0.05, vol)
                
                price = black_scholes(underlying_spot, strike, T, r, vol, opt_type)
                return round(price, 2)
        except Exception as e:
            pass
            
    return None

