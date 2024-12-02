import requests
import time

# Parâmetros da API
symbol = "BTCUSDT"
interval = "15m"
limit = 1000

# Exemplo de timestamps em segundos, converta para milissegundos
start_time_seconds = 1731414339
end_time_seconds = 1731500000

start_time_ms = start_time_seconds * 1000
end_time_ms = end_time_seconds * 1000

# Realiza a requisição
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": symbol,
    "interval": interval,
    "limit": limit,
    "startTime": start_time_ms,
    "endTime": end_time_ms
}

response = requests.get(url, params=params)
data = response.json()

# Verificar se os dados foram retornados
if data:
    print("Dados recebidos com sucesso!")
    print(data)
else:
    print("A resposta veio vazia. Verifique os parâmetros.")
