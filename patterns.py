def detect_patterns(df):
    patterns = []
    for i in range(2, len(df)-2):
        o, h, l, c = df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]
        prev_c = df['Close'][i-1]
        next_c = df['Close'][i+1]

        if c> o and c> prev_c and df['Open'][i-1]> df['Close'][i-1]:
            patterns.append(('bullish_engulfing', df.index[i]))
        elif c < o and c < prev_c and df['Open'][i-1] < df['Close'][i-1]:
            patterns.append(('bearish_engulfing', df.index[i]))
        # Add 14 more patterns here...
    return patterns
