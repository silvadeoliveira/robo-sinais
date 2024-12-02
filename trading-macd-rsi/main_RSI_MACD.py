import pandas as pd
import ta
import requests
import time
from salvar_historico_sqlite import criar_banco_dados, salvar_operacao_sqlite
import datetime
import calendar

# Nome do banco de dados
nome_banco_sqlite = "historico_main_RSI_MACD_trades.db"

# Criar banco de dados
criar_banco_dados(nome_banco_sqlite)

# Função para obter candles da Binance
def obter_candles(symbol, interval, limit, start_time_ms=None, end_time_ms=None):
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
        df = pd.DataFrame(response.json(), columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = df["close"].astype(float)
        return df
    else:
        print("Erro ao buscar dados da API:", response.text)
        return pd.DataFrame()

# Estratégia de trading baseada em MACD e RSI
def calculate_indicators(data):
    # Cálculo do RSI
    data['rsi'] = ta.momentum.RSIIndicator(data['close'], window=14).rsi()
    
    # Cálculo do MACD
    macd = ta.trend.MACD(data['close'], window_slow=26, window_fast=12, window_sign=9)
    data['macd'] = macd.macd()
    data['signal'] = macd.macd_signal()
    data['macd_hist'] = macd.macd_diff()
    
    # Sinais de compra e venda
    data['buy_signal'] = (data['rsi'] < 30) & (data['macd'] > data['signal'])
    data['sell_signal'] = (data['rsi'] > 70) & (data['macd'] < data['signal'])
    return data

# Determinar valores de compra, stop loss e take profit
def determine_trade_values(data):
    last_row = data.iloc[-1]
    if last_row['buy_signal']:
        close_price = last_row['close']
        stop_loss = close_price * 0.99  # 1% abaixo do preço de compra
        take_profit = close_price * 1.015  # 1.5% acima do preço de compra
        print(f"Sinal de COMPRA detectado:")
        print(f"Preço de Compra: {close_price:.2f}")
        print(f"Stop Loss: {stop_loss:.2f}")
        print(f"Take Profit: {take_profit:.2f}")
        return "BUY", close_price, stop_loss, take_profit
    elif last_row['sell_signal']:
        print(f"Sinal de VENDA detectado no preço de fechamento: {last_row['close']:.2f}")
        return "SELL", last_row['close'], None, None
    else:
        print("Sem sinais de compra ou venda.")
        return "HOLD", None, None, None

# Função para registrar operação no SQLite
def registrar_no_sqlite(data_hora, operacao, preco, stop_loss, take_profit):
    salvar_operacao_sqlite(nome_banco_sqlite, data_hora, operacao, preco, stop_loss, take_profit)

# Função principal
def main():
    symbol = "BTCUSDT"
    interval = "1h"
    limit = 100
    
    while True:
        try:
            # Obter dados do mercado
            dt_end_time = datetime.datetime.now()
            end_time = calendar.timegm(dt_end_time.timetuple()) + (3 * 60 * 60)
            last_time = 48 * 60 * 60
            start_time = end_time - last_time
             # Converter timestamps para milissegundos
            start_time_ms = start_time * 1000
            end_time_ms = end_time * 1000

            market_data = obter_candles(symbol, interval, limit,start_time_ms,end_time_ms)
            
            if market_data.empty:
                print("Nenhum dado retornado, tentando novamente...")
                time.sleep(15)
                continue
            
            # Calcular indicadores e sinais
            market_data = calculate_indicators(market_data)
            
            # Determinar valores de trade
            trade_signal, price, stop_loss, take_profit = determine_trade_values(market_data)
            
            # Registrar operação no banco de dados
            if trade_signal in ["BUY", "SELL"] and price is not None:
                data_hora = market_data.iloc[-1]['timestamp']
                registrar_no_sqlite(data_hora, trade_signal, price, stop_loss, take_profit)
                print(f"Operação registrada: {trade_signal} em {price:.2f}")
            else:
                print("Nenhuma operação registrada.")
            
            # Aguardar antes de nova atualização
            time.sleep(3600)  # Atualiza a cada hora
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(15)

# Executa o script
if __name__ == "__main__":
    main()