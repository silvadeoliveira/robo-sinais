import pandas as pd

def calcular_macd(cotacoes, periodo_longo=26, periodo_curto=12, periodo_sinal=9):
    """
    Calcula o MACD (linha MACD e linha de sinal).
    :param cotacoes: Lista de preços de fechamento.
    :param periodo_longo: Período da média móvel longa.
    :param periodo_curto: Período da média móvel curta.
    :param periodo_sinal: Período da média móvel da linha de sinal.
    :return: Tupla com duas listas: linha MACD e linha de sinal.
    """
    df = pd.DataFrame({'Close': cotacoes})
    df['EMA_Curta'] = df['Close'].ewm(span=periodo_curto, adjust=False).mean()
    df['EMA_Longa'] = df['Close'].ewm(span=periodo_longo, adjust=False).mean()
    df['MACD'] = df['EMA_Curta'] - df['EMA_Longa']
    df['Sinal'] = df['MACD'].ewm(span=periodo_sinal, adjust=False).mean()
    return df['MACD'].tolist(), df['Sinal'].tolist()

def calcular_rsi(cotacoes, periodo=14):
    """
    Calcula o RSI (Relative Strength Index).
    :param cotacoes: Lista de preços de fechamento.
    :param periodo: Período para cálculo do RSI.
    :return: Lista com valores do RSI.
    """
    df = pd.DataFrame({'Close': cotacoes})
    df['Delta'] = df['Close'].diff()
    df['Ganhos'] = df['Delta'].clip(lower=0)
    df['Perdas'] = -df['Delta'].clip(upper=0)

    df['Media_Ganhos'] = df['Ganhos'].rolling(window=periodo).mean()
    df['Media_Perdas'] = df['Perdas'].rolling(window=periodo).mean()

    df['RS'] = df['Media_Ganhos'] / df['Media_Perdas']
    df['RSI'] = 100 - (100 / (1 + df['RS']))
    return df['RSI'].tolist()
