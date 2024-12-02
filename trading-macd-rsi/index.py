import datetime
import calendar
import requests
import json
import matplotlib.pyplot as plt
import sys
import time
sys.path.append('/polosdk')
from polosdk import SpotRestClient


#dataInical = datetime.datetime.utcfromtimestamp("10-11-2024").strftime("%d-%m-y")
data_to_ts = lambda x: calendar.timegm((datetime.datetime.strptime(x, "%d-%m-%Y")).timetuple())

# Parâmetros da API
symbol = "BTCUSDT"
interval = "15m"
limit = 1000
url = "https://api.binance.com/api/v3/klines"

APIKey = "9EOHXCSL-DPZKMG0L-P181OK3U-B3OOQLDB"
SecretKey = "5686764edce88c977471e9779d92b5dcc5dc008633ffdc431a934e092bf89f338310fea8edd98a08de430d8a31a8e4251331795830f462177c0575ef7968ca13"




#plt.ion()

AGUARDANDO_SINAL_COMPRA = 0
AGUARDANDO_SINAL_VENDA = 1
estado = AGUARDANDO_SINAL_COMPRA
compras = []
vendas = []
while True:
    dtEndTime = datetime.datetime.now()
    endTime= calendar.timegm(dtEndTime.timetuple()) + (3 * 60 * 60)
    lastTime = 48 * 60 * 60
    startTime = endTime - lastTime

    start_time_ms = startTime * 1000
    end_time_ms = endTime * 1000
    params = {
    "symbol": symbol,
    "interval": interval,
    "limit": limit,
   "startTime": start_time_ms,
   "endTime": end_time_ms
    }

    response = requests.get(url, params=params)
   
    data = json.loads(response.text)
    cotacoes = []
    for e in data:
        cotacoes.append(float(e[4]))
   
    print(cotacoes[-1:])
    mediaRapida = [sum(cotacoes[-8:] ) / 8]  * len(cotacoes)
    medialenta = [sum(cotacoes[-21:] ) / 21]  * len(cotacoes)

    if estado == AGUARDANDO_SINAL_COMPRA:
            if mediaRapida[0] > medialenta[0] + (medialenta[0] * 0.0025):
                compras.append(medialenta[0] * 0.0025)
                print(datetime.datetime.now())
                print("compra")
                estado = AGUARDANDO_SINAL_VENDA
    elif estado == AGUARDANDO_SINAL_VENDA:
        if mediaRapida[0] < medialenta[0] - (medialenta[0] * 0.0025):
            print(datetime.datetime.now())
            print("venda")
            vendas.append(medialenta[0] * 0.0025)
            estado = AGUARDANDO_SINAL_COMPRA
    print(datetime.datetime.now())
    print("Total de vendas: " + str(sum(vendas)))
    print("Total de compras: " + str(sum(compras)))
    print("cotação: "+ str(cotacoes[-1:]))
    time.sleep(15)

'''
    ag = plt.gca()
    ag.clear()
    plt.plot(cotacoes[-50:])
    plt.plot(mediaRapida[-50:], color="red")
    plt.plot(medialenta[-50:], color="green")
    plt.draw()

    plt.pause(5)

'''

client = SpotRestClient(APIKey,SecretKey)
def pagaPrecodeCompra(moeda):
    try:
        return client.markets().get_prices()
    except:
        return None


print(pagaSaldo("teste"))
##response = client.get_market('BTC_USDT')
def pagaSaldo(moeda):
    try:
        return client.markets().get_prices()
    except:
        return None




