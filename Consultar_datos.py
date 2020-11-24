import requests
import json
apiKey = "55A5SUC3FX5Y4F6N"
#empresas=["IBM","EPM","EC","CIB"]
empresas=["IBM","EC"]

detalleEmpresas=[]
gananciasAnuales=[]
banlancesAnuales=[]
historicos=[]

#Historico de transacciones ultimo mes
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=demo

#balances anuales y trimestrales
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=55A5SUC3FX5Y4F6N&datatype=json

#Ganancias por año y trimestral
#https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo

#Historico de tasa de cambio de dolar a peso colombiano cada 5 min
#https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=COP&interval=5min&apikey=55A5SUC3FX5Y4F6N&datatype=csv&outputsize=full

#informacion de lo empresa
#https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
for emp in empresas:
    #consultamos informacion de la empresa
    reqEmp = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol='+emp+'&apikey='+apiKey)
    reqStatus=reqEmp.status_code

    if reqStatus==200:
        detalleEmpresas.append(reqEmp.json())

    # consultamos Historico de transacciones ultimo mes
    reqHistorico = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+emp+'&apikey=' + apiKey)
    reqStatus = reqHistorico.status_code

    if reqStatus == 200:
        historicos.append(reqHistorico.json())

    #consultamos Ganancias por año y trimestral
    reqGanan = requests.get('https://www.alphavantage.co/query?function=EARNINGS&symbol='+emp+'&apikey='+apiKey)
    reqStatus=reqGanan.status_code

    if reqStatus==200:
        gananciasAnuales.append(reqGanan.json())

    #consultamos balances por año y trimestral
    reqbalances = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+emp+'&outputsize=full&apikey='+apiKey+'&datatype=json')
    reqStatus=reqbalances.status_code

    if reqStatus==200:
        banlancesAnuales.append(reqbalances.json())

with open('detalleEmpresas.json', 'w') as file:
    json.dump(detalleEmpresas, file, indent=4)

with open('gananciasAnuales.json', 'w') as file:
    json.dump(gananciasAnuales, file, indent=4)

with open('banlancesAnuales.json', 'w') as file:
    json.dump(banlancesAnuales, file, indent=4)

with open('historicos.json', 'w') as file:
    json.dump(historicos, file, indent=4)