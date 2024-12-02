import pandas as pd

def calcular_ema(cotacoes, periodo):
    """
    Calcula a Média Móvel Exponencial (EMA).
    :param cotacoes: Lista de preços de fechamento.
    :param periodo: Período para cálculo da EMA.
    :return: Lista com valores da EMA.
    """
    return pd.Series(cotacoes).ewm(span=periodo, adjust=False).mean().tolist()
