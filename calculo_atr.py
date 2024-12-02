import pandas as pd

def calcular_atr(candles, periodo=14):
    """
    Calcula o Average True Range (ATR).
    :param candles: Lista de candles (OHLC). Cada elemento é [open, high, low, close].
    :param periodo: Período para cálculo do ATR.
    :return: ATR calculado como uma lista.
    """
    high = [c[1] for c in candles]
    low = [c[2] for c in candles]
    close = [c[3] for c in candles]
    
    df = pd.DataFrame({
        'High': high,
        'Low': low,
        'Close': close
    })
    df['TR'] = pd.concat([
        df['High'] - df['Low'],
        abs(df['High'] - df['Close'].shift(1)),
        abs(df['Low'] - df['Close'].shift(1))
    ], axis=1).max(axis=1)
    df['ATR'] = df['TR'].rolling(window=periodo).mean()
    return df['ATR'].tolist()
