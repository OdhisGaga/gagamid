from ta import momentum, trend, volatility
from patterns import detect_patterns

def apply_indicators(df):
    df['rsi'] = momentum.RSIIndicator(df['Close']).rsi()
    df['macd'] = trend.macd_diff(df['Close'])
    df['sma'] = trend.SMAIndicator(df['Close'], window=20).sma_indicator()
    df['ema'] = trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['atr'] = volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
    return df

def generate_signal(df):
    df = apply_indicators(df)
    patterns = detect_patterns(df)
    signal = 'HOLD'
    last_price = df['Close'].iloc[-1]
    reward_ratio = (df['High'].max() - last_price) / (last_price - df['Low'].min())

    if df['rsi'].iloc[-1] < 30 and df['macd'].iloc[-1]> 0 and reward_ratio>= 2.5:
        signal = 'BUY'
    elif df['rsi'].iloc[-1]> 70 and df['macd'].iloc[-1] < 0 and reward_ratio>= 2.5:
        signal = 'SELL'

    for pattern, _ in patterns[-5:]:
        if pattern.startswith('bullish') and reward_ratio>= 2.5:
            signal = 'BUY'
        elif pattern.startswith('bearish') and reward_ratio>= 2.5:
            signal = 'SELL'

    return signal

import pandas as pd

def detect_levels(df, window=20):
    support, resistance = [], []
    for i in range(window, len(df)-window):
        low_range = df['Low'][i-window:i+window]
        high_range = df['High'][i-window:i+window]
        if df['Low'][i] == low_range.min():
            support.append((df.index[i], df['Low'][i]))
        if df['High'][i] == high_range.max():
            resistance.append((df.index[i], df['High'][i]))
    return support, resistance

def detect_zones(df):
    zones = []
    for i in range(2, len(df)-2):
        if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1]:
            zones.append(('demand', df.index[i], df['Low'][i]))
        elif df['High'][i]> df['High'][i-1] and df['High'][i]> df['High'][i+1]:
            zones.append(('supply', df.index[i], df['High'][i]))
    return zones

def detect_liquidity_sweeps(df):
    sweeps = []
    for i in range(1, len(df)-1):
        if df['Low'][i] < df['Low'][i-1] and df['Close'][i]> df['Open'][i]:
            sweeps.append(('bullish_sweep', df.index[i]))
        elif df['High'][i]> df['High'][i-1] and df['Close'][i] < df['Open'][i]:
            sweeps.append(('bearish_sweep', df.index[i]))
    return sweeps

def generate_signal(df):
    support, resistance = detect_levels(df)
    zones = detect_zones(df)
    sweeps = detect_liquidity_sweeps(df)
    last_price = df['Close'].iloc[-1]
    signal = 'HOLD'

    for zone_type, _, level in zones[-5:]:
        if zone_type == 'demand' and last_price < level:
            signal = 'BUY'
        elif zone_type == 'supply' and last_price> level:
            signal = 'SELL'

    for sweep_type, _ in sweeps[-5:]:
        if sweep_type == 'bullish_sweep':
            signal = 'BUY'
        elif sweep_type == 'bearish_sweep':
            signal = 'SELL'

    return signal
