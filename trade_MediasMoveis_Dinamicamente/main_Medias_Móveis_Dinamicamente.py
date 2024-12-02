import datetime
import calendar
import requests
import pandas as pd
import time
from salvar_historico_sqlite import criar_banco_dados, salvar_operacao_sqlite

# Nome do banco de dados
nome_banco_sqlite = "historico_trades.db"

# Criar banco de dados
criar_banco_dados(nome_banco_sqlite)

# Função para registrar operação no SQLite
def registrar_no_sqlite(data_hora, operacao, preco, stop_loss, take_profit):
    salvar_operacao_sqlite(nome_banco_sqlite, data_hora, operacao, preco, stop_loss, take_profit)

# Função para converter datas para timestamp
data_to_ts = lambda x: calendar.timegm(datetime.datetime.strptime(x, "%d-%m-%Y").timetuple())

# Parâmetros da API
symbol = "BTCUSDT"
interval = "15m"
limit = 1000
url = "https://api.binance.com/api/v3/klines"

# Estados de negociação
AGUARDANDO_SINAL_COMPRA = 0
AGUARDANDO_SINAL_VENDA = 1
estado = AGUARDANDO_SINAL_COMPRA

# Função para obter cotações da Binance
def obter_cotacoes():
    dtEndTime = datetime.datetime.now()
    endTime = calendar.timegm(dtEndTime.timetuple()) + (3 * 60 * 60)
    startTime = endTime - (48 * 60 * 60)  # Últimas 48 horas
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": startTime * 1000,
        "endTime": endTime * 1000
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    cotacoes = [float(e[4]) for e in data]
    return cotacoes

# Loop principal para processar as operações
while True:
    try:
        cotacoes = obter_cotacoes()
        df = pd.DataFrame({"close": cotacoes})
        df["SMA_8"] = df["close"].rolling(window=8).mean()
        df["SMA_21"] = df["close"].rolling(window=21).mean()
        
        if len(df) < 21:
            print("Dados insuficientes para calcular médias móveis. Aguardando mais dados...")
            time.sleep(15)
            continue
        
        SMA_8 = df["SMA_8"].iloc[-1]
        SMA_21 = df["SMA_21"].iloc[-1]
        close_price = df["close"].iloc[-1]
        
        if estado == AGUARDANDO_SINAL_COMPRA:
            if SMA_8 > SMA_21 * 1.0025:
                stop_loss = close_price * 0.99  # 1% abaixo do preço de compra
                take_profit = close_price * 1.015  # 1.5% acima do preço de compra
                registrar_no_sqlite(datetime.datetime.now(), "BUY", close_price, stop_loss, take_profit)
                print(f"Compra registrada em {datetime.datetime.now()}: Preço = {close_price:.2f}, Stop Loss = {stop_loss:.2f}, Take Profit = {take_profit:.2f}")
                estado = AGUARDANDO_SINAL_VENDA
        
        elif estado == AGUARDANDO_SINAL_VENDA:
            if SMA_8 < SMA_21 * 0.9975:
                stop_loss = None
                take_profit = None
                registrar_no_sqlite(datetime.datetime.now(), "SELL", close_price, stop_loss, take_profit)
                print(f"Venda registrada em {datetime.datetime.now()}: Preço = {close_price:.2f}")
                estado = AGUARDANDO_SINAL_COMPRA
        
        print(f"Estado atual: {'Compra' if estado == AGUARDANDO_SINAL_COMPRA else 'Venda'}")
        print(f"Última cotação: {close_price:.2f}")
        
        time.sleep(15)
    
    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(15)
