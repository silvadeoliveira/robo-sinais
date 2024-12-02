import datetime
import calendar
import requests
import json
import time
import matplotlib.pyplot as plt

# Função para converter data para timestamp
def data_to_ts(data_str: str) -> int:
    return calendar.timegm(datetime.datetime.strptime(data_str, "%d-%m-%Y").timetuple())

# Função para calcular médias móveis
def calcular_media_movel(cotacoes, periodo):
    return [sum(cotacoes[i - periodo:i]) / periodo for i in range(periodo, len(cotacoes) + 1)]

# Função para buscar dados da API
def obter_cotacoes(symbol, interval, limit, start_time_ms, end_time_ms):
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
        return [float(candle[4]) for candle in json.loads(response.text)]
    else:
        print("Erro ao buscar dados da API:", response.text)
        return []

# Função para plotar os dados
def plotar_cotacoes(cotacoes, media_rapida, media_lenta, compras, vendas):
    plt.figure(figsize=(12, 6))
    plt.plot(cotacoes, label='Preço Fechamento', color='blue')
    plt.plot(range(len(cotacoes) - len(media_rapida), len(cotacoes)), media_rapida, label='Média Rápida (8)', color='green')
    plt.plot(range(len(cotacoes) - len(media_lenta), len(cotacoes)), media_lenta, label='Média Lenta (21)', color='red')
    
    # Marcar compras e vendas
    for compra in compras:
        plt.scatter(compra[0], compra[1], label='Compra', color='lime', marker='^')
    for venda in vendas:
        plt.scatter(venda[0], venda[1], label='Venda', color='orange', marker='v')
    
    plt.legend()
    plt.title('Preço e Médias Móveis com Sinais')
    plt.xlabel('Período')
    plt.ylabel('Preço')
    plt.grid(True)
    plt.show()

# Constantes de estado
AGUARDANDO_SINAL_COMPRA = 0
AGUARDANDO_SINAL_VENDA = 1

# Variáveis globais
estado = AGUARDANDO_SINAL_COMPRA
compras = []
vendas = []

symbol = "BTCUSDT"
interval = "15m"
limit = 1000

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

        # Obter cotações
        cotacoes = obter_cotacoes(symbol, interval, limit, start_time_ms, end_time_ms)

        if len(cotacoes) < 21:  # Verificar se há cotações suficientes
            print("Dados insuficientes para cálculo de médias móveis.")
            time.sleep(15)
            continue

        # Calcular médias móveis
        media_rapida = calcular_media_movel(cotacoes, 8)
        media_lenta = calcular_media_movel(cotacoes, 21)

        # Pegar os últimos valores das médias móveis
        ultima_media_rapida = media_rapida[-1]
        ultima_media_lenta = media_lenta[-1]

        # Estratégia de compra/venda
        if estado == AGUARDANDO_SINAL_COMPRA:
            if ultima_media_rapida > ultima_media_lenta + (ultima_media_lenta * 0.0025):
                compras.append((len(cotacoes) - 1, cotacoes[-1]))
                print(f"{datetime.datetime.now()} - Sinal de COMPRA: {cotacoes[-1]}")
                estado = AGUARDANDO_SINAL_VENDA
        elif estado == AGUARDANDO_SINAL_VENDA:
            if ultima_media_rapida < ultima_media_lenta - (ultima_media_lenta * 0.0025):
                vendas.append((len(cotacoes) - 1, cotacoes[-1]))
                print(f"{datetime.datetime.now()} - Sinal de VENDA: {cotacoes[-1]}")
                estado = AGUARDANDO_SINAL_COMPRA

        # Exibir resumo
        print(f"Total de compras: {len(compras)}, Total de vendas: {len(vendas)}")
        print(f"Cotação atual: {cotacoes[-1]}")

        # Plotar gráficos a cada ciclo
        plotar_cotacoes(cotacoes, media_rapida, media_lenta, compras, vendas)

        time.sleep(15)

    except Exception as e:
        print("Erro:", e)
        time.sleep(15)
