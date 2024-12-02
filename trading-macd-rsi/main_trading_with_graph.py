import datetime
import calendar
import requests
import time
import matplotlib.pyplot as plt
from calculo_ema import calcular_ema
from calculo_atr import calcular_atr
from gerenciamento_risco import GerenciamentoRisco
from salvar_historico_sqlite import criar_banco_dados, salvar_operacao_sqlite
# Nome do banco de dados
nome_banco_sqlite = "historico_trades.db"

# Criar banco de dados
criar_banco_dados(nome_banco_sqlite)

# Função para registrar operação no SQLite
def registrar_no_sqlite(data_hora, operacao, preco, stop_loss, take_profit):
    salvar_operacao_sqlite(nome_banco_sqlite, data_hora, operacao, preco, stop_loss, take_profit)

# Função para buscar dados da API
def obter_candles(symbol, interval, limit, start_time_ms, end_time_ms):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": start_time_ms,
        "endTime": end_time_ms
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [[float(c[1]), float(c[2]), float(c[3]), float(c[4])] for c in response.json()]
    else:
        print("Erro ao buscar dados da API:", response.text)
        return []

def inicializar_grafico():
    """
    Inicializa a janela de gráfico e retorna os objetos necessários para atualizações.
    """
    plt.ion()  # Ativa o modo interativo
    fig, ax = plt.subplots(figsize=(14, 7))  # Cria uma figura e eixos
    return fig, ax

def atualizar_grafico(ax, cotacoes, ema_rapida, ema_lenta, compras, vendas):
    """
    Atualiza o gráfico com os dados mais recentes.
    """
    ax.clear()  # Limpa o conteúdo do gráfico
    ax.plot(cotacoes, label='Preço de Fechamento', color='blue')
    ax.plot(range(len(cotacoes) - len(ema_rapida), len(cotacoes)), ema_rapida, label='EMA Rápida (8)', color='green')
    ax.plot(range(len(cotacoes) - len(ema_lenta), len(cotacoes)), ema_lenta, label='EMA Lenta (21)', color='red')

    # Sinais de Compra
    for compra in compras:
        ax.scatter(compra[0], compra[1], color='lime', label='Compra', marker='^', s=100)
    
    # Sinais de Venda
    for venda in vendas:
        ax.scatter(venda[0], venda[1], color='orange', label='Venda', marker='v', s=100)

    ax.set_title('Trading com Médias Móveis e ATR')
    ax.set_xlabel('Tempo (em intervalos)')
    ax.set_ylabel('Preço')
    ax.legend(loc='best')
    ax.grid(True)
    plt.pause(0.01)  # Atualiza o gráfico sem bloquear

# Função para plotar os dados
def plotar_dados(cotacoes, ema_rapida, ema_lenta, compras, vendas):
    plt.figure(figsize=(14, 7))
    plt.plot(cotacoes, label='Preço de Fechamento', color='blue')
    plt.plot(range(len(cotacoes) - len(ema_rapida), len(cotacoes)), ema_rapida, label='EMA Rápida (8)', color='green')
    plt.plot(range(len(cotacoes) - len(ema_lenta), len(cotacoes)), ema_lenta, label='EMA Lenta (21)', color='red')

    # Sinais de Compra
    for compra in compras:
        plt.scatter(compra[0], compra[1], color='lime', label='Compra', marker='^', s=100)
    
    # Sinais de Venda
    for venda in vendas:
        plt.scatter(venda[0], venda[1], color='orange', label='Venda', marker='v', s=100)
    
    plt.title('Trading com Médias Móveis e ATR')
    plt.xlabel('Tempo (em intervalos)')
    plt.ylabel('Preço')
    plt.legend(loc='best')
    plt.grid()
    #plt.show()
    plt.pause(0.01)  # Pausa breve para atualização do gráfico

# Constantes de estado
AGUARDANDO_SINAL_COMPRA = 0
AGUARDANDO_SINAL_VENDA = 1

# Configurações
symbol = "BTCUSDT"
interval = "15m"
limit = 1000
estado = AGUARDANDO_SINAL_COMPRA
compras = []
vendas = []

# Inicializar o gerenciamento de risco
risco = GerenciamentoRisco(stop_loss_percent=0.01, take_profit_percent=0.02)
# Inicializar gráfico fora do loop
fig, ax = inicializar_grafico()
# Loop principal
while True:
    try:
        dt_end_time = datetime.datetime.now()
        end_time = calendar.timegm(dt_end_time.timetuple()) + (3 * 60 * 60)
        last_time = 48 * 60 * 60
        start_time = end_time - last_time

        # Converter timestamps para milissegundos
        start_time_ms = start_time * 1000
        end_time_ms = end_time * 1000

        # Obter candles (OHLC)
        candles = obter_candles(symbol, interval, limit, start_time_ms, end_time_ms)
        if len(candles) < 21:  # Verificar se há dados suficientes
            print("Dados insuficientes para cálculo.")
            time.sleep(15)
            continue

        # Extrair preços de fechamento
        cotacoes = [c[3] for c in candles]

        # Calcular EMA e ATR
        ema_rapida = calcular_ema(cotacoes, 8)
        ema_lenta = calcular_ema(cotacoes, 21)
        atr = calcular_atr(candles, periodo=14)

        # Usar os últimos valores calculados
        ultima_ema_rapida = ema_rapida[-1]
        ultima_ema_lenta = ema_lenta[-1]
        ultimo_atr = atr[-1]
        print("ultima_ema_rapida:" + str(ultima_ema_rapida))
        print("ultima_ema_lenta:" + str(ultima_ema_lenta))
        print("ultimo_atr:" + str(ultimo_atr))

        # Estratégia de compra/venda
        if estado == AGUARDANDO_SINAL_COMPRA:
            if ultima_ema_rapida > ultima_ema_lenta + (ultimo_atr * 0.25):
                preco_compra = cotacoes[-1]
                risco.definir_niveis(preco_compra)
                compras.append((len(cotacoes) - 1, preco_compra))
                print(f"{datetime.datetime.now()} - Sinal de COMPRA: {preco_compra}")
                print(f"Stop-Loss: {risco.stop_loss}, Take-Profit: {risco.take_profit}")
                estado = AGUARDANDO_SINAL_VENDA
                registrar_no_sqlite(datetime.datetime.now(), "COMPRA", preco_compra, risco.stop_loss, risco.take_profit)
        elif estado == AGUARDANDO_SINAL_VENDA:
            preco_atual = cotacoes[-1]
            status_saida = risco.verificar_saida(preco_atual)
            if status_saida == "STOP_LOSS" or status_saida == "TAKE_PROFIT":
                vendas.append((len(cotacoes) - 1, preco_atual))
                print(f"{datetime.datetime.now()} - Sinal de VENDA ({status_saida}): {preco_atual}")
                estado = AGUARDANDO_SINAL_COMPRA
                registrar_no_sqlite(datetime.datetime.now(), "VENDA", preco_atual, risco.stop_loss, risco.take_profit)

        # Exibir resumo
        print(f"Total de Compras: {len(compras)} - Total de Vendas: {len(vendas)}")
        print(f"Cotação Atual: {cotacoes[-1]}")

        # Plotar dados após cada iteração
        atualizar_grafico(ax, cotacoes, ema_rapida, ema_lenta, compras, vendas)

        print("\nAguardando a próxima atualização...\n" + "-" * 30)
        #print("\n--------------------\n")

        time.sleep(15)

    except Exception as e:
        print("Erro:", e)
        time.sleep(15)
