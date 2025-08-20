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

