import matplotlib.pyplot as plt

# Inicializar figura e eixos fora da função para reutilização
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

def plotar_macd_rsi_unificado(cotacoes, macd, sinal, rsi, compras=None, vendas=None):
    """
    Atualiza dinamicamente um único gráfico com subplots para Preço, MACD e RSI.
    :param cotacoes: Lista de preços de fechamento.
    :param macd: Lista de valores do MACD.
    :param sinal: Lista de valores da linha de sinal.
    :param rsi: Lista de valores do RSI.
    :param compras: Lista de índices de compras (opcional).
    :param vendas: Lista de índices de vendas (opcional).
    """
    compras = compras or []
    vendas = vendas or []

    # Subplot 1: Preço Fechamento com Sinais
    axs[0].cla()  # Limpa apenas este eixo
    axs[0].plot(cotacoes, label='Preço Fechamento', color='blue', alpha=0.6)
    for idx in compras:
        axs[0].scatter(idx, cotacoes[idx], label='Compra', color='green', marker='^')
    for idx in vendas:
        axs[0].scatter(idx, cotacoes[idx], label='Venda', color='red', marker='v')
    axs[0].set_title('Preço Fechamento com Sinais de Compra e Venda')
    axs[0].set_ylabel('Preço')
    axs[0].legend()
    axs[0].grid()

    # Subplot 2: MACD e Linha de Sinal
    axs[1].cla()  # Limpa apenas este eixo
    axs[1].plot(macd, label='MACD', color='purple', alpha=0.6)
    axs[1].plot(sinal, label='Linha de Sinal', color='orange', alpha=0.6)
    axs[1].axhline(0, color='black', linewidth=0.8, linestyle='--')
    axs[1].set_title('MACD e Linha de Sinal')
    axs[1].set_ylabel('MACD')
    axs[1].legend()
    axs[1].grid()

    # Subplot 3: RSI
    axs[2].cla()  # Limpa apenas este eixo
    axs[2].plot(rsi, label='RSI', color='brown', alpha=0.6)
    axs[2].axhline(70, color='red', linewidth=0.8, linestyle='--', label='Sobrecomprado (70)')
    axs[2].axhline(30, color='green', linewidth=0.8, linestyle='--', label='Sobrevendido (30)')
    axs[2].set_title('RSI')
    axs[2].set_xlabel('Período')
    axs[2].set_ylabel('RSI')
    axs[2].legend()
    axs[2].grid()

    # Atualizar a figura
    plt.tight_layout()
    plt.pause(0.01)  # Atualiza o gráfico sem bloquear
