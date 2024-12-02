import pandas as pd
import matplotlib.pyplot as plt

def plotar_macd_rsi(cotacoes, macd, sinal, rsi, compras=None, vendas=None):
    """
    Plota o gráfico do preço, MACD, RSI e marca sinais de compra e venda.
    :param cotacoes: Lista de preços de fechamento.
    :param macd: Lista de valores do MACD.
    :param sinal: Lista de valores da linha de sinal.
    :param rsi: Lista de valores do RSI.
    :param compras: Lista de índices de compras (opcional).
    :param vendas: Lista de índices de vendas (opcional).
    """
    compras = compras or []
    vendas = vendas or []

    # Converter em DataFrame para plotagem
    df = pd.DataFrame({'Close': cotacoes, 'MACD': macd, 'Sinal': sinal, 'RSI': rsi})

    # Plotar preço e sinais
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Preço Fechamento', color='blue', alpha=0.6)
    for idx in compras:
        plt.scatter(idx, df['Close'].iloc[idx], label='Compra', color='green', marker='^')
    for idx in vendas:
        plt.scatter(idx, df['Close'].iloc[idx], label='Venda', color='red', marker='v')
    plt.title('Preço Fechamento com Sinais de Compra e Venda')
    plt.xlabel('Período')
    plt.ylabel('Preço')
    plt.legend()
    plt.grid()
    plt.pause(0.01)  # Atualiza o gráfico sem bloquear

    # Plotar MACD
    plt.figure(figsize=(14, 7))
    plt.plot(df['MACD'], label='MACD', color='purple', alpha=0.6)
    plt.plot(df['Sinal'], label='Linha de Sinal', color='orange', alpha=0.6)
    plt.title('MACD e Linha de Sinal')
    plt.xlabel('Período')
    plt.ylabel('Valor MACD')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.legend()
    plt.grid()
    plt.pause(0.01)  # Atualiza o gráfico sem bloquear

    # Plotar RSI
    plt.figure(figsize=(14, 7))
    plt.plot(df['RSI'], label='RSI', color='brown', alpha=0.6)
    plt.axhline(70, color='red', linewidth=0.8, linestyle='--', label='Sobrecomprado (70)')
    plt.axhline(30, color='green', linewidth=0.8, linestyle='--', label='Sobrevendido (30)')
    plt.title('RSI')
    plt.xlabel('Período')
    plt.ylabel('Valor RSI')
    plt.legend()
    plt.grid()
    plt.pause(0.01)  # Atualiza o gráfico sem bloquear
