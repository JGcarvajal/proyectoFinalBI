import requests
import json
from os import remove
import boto3
import time
from datetime import datetime

#proyecto final de BUSINESS INTELLIGENCE BI
#presetado por Juan Gabriel Carvajal H - Jhon Alexander Cruz B.
#Ingenieria de Sistemas y Computacion
#Para el desarrollos del proyecto se consultara
#la aplicacion Alpha Vantage

#La apikey nos permite acceder ala aplicacion.
#para obterner la informacion necesaria para el proyecto.

#sudo apt-get install python3-boto3

apiKey = "55A5SUC3FX5Y4F6N"

#por medio de la aplicacion Alpha Vantage se puede consutar
#la informacion de varias empresas en este caso se consultaran
#estas 4 empresa IBM, EPM, ECOPETROL "EC", BANCOLOMBIA "CIB"

empresas=["IBM","EPM","EC","CIB"]
#empresas=["EC"]
objetosJson=['detalleEmpresas','gananciasAnuales','banlancesAnuales','historicos','cambioMoneda']
#Al consultar en la aplicancion el endpoint Query se
#extrae la informacion necesaria y se adiciona a los
#documentos.

detalleEmpresas=[]
gananciasAnuales=[]
banlancesAnuales=[]
historicos=[]
cambioMoneda=[]

#Creamos el cliente de S3
s3_client=boto3.client('s3',aws_access_key_id='AKIAZKHZZ4X2FVILOE6L',aws_secret_access_key="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")

#URL para obtener la informacion de la plicacion
#y porder manipular los datos son las siguientes.

#url para obtener Historico de transacciones ultimo mes
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=demo


#url para obtener balances anuales y trimestrales
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=55A5SUC3FX5Y4F6N&datatype=json

#url para obtener Ganancias por año y trimestral
#https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo

#url para obtener Historico de tasa de cambio de dolar a peso colombiano cada 5 min
#https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=COP&interval=5min&apikey=55A5SUC3FX5Y4F6N&datatype=csv&outputsize=full

#url para obtener la informacion de la empresa
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

    #esperamos 60 segundos por restriccion del api
    time.sleep(60)

    print("Consultamos la empresa "+emp+ ", en 60 segundos consultamos la siguiente")

#Historico de tasa de cambio de dolar a peso colombiano cada 5 min
reqcambio = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=COP&interval=5min&apikey=55A5SUC3FX5Y4F6N&datatype=json&outputsize=full')
reqStatus=reqcambio.status_code
if reqStatus==200:
    cambioMoneda.append(reqcambio.json())

#enviamos los archivos a S3
fecha=datetime.now().strftime("%Y%m%d%S%M%S")
json_object=[]
for i in range(5):
    print("i="+i)
    #'detalleEmpresas','gananciasAnuales','banlancesAnuales','historicos','cambioMoneda']
    #s3_client.put_object(Body=str(json.dumps(detalleEmpresas)),Bucket='proyecto-final-bi-jgc-jac', Key='detalleEmpresas.json' )
    if i==1:
        json_object = detalleEmpresas
    elif i== 2:
        json_object = gananciasAnuales
    elif i== 3:
        json_object = banlancesAnuales
    elif i== 4:
        json_object = historicos
    elif i == 5:
        json_object = cambioMoneda

    s3_client.put_object(
        Body=str(json.dumps(json_object)),
        Bucket='proyecto-final-bi-jgc-jac',
        Key='api/alphavantage/'+objetosJson(i)+'/'+objetosJson(i)+'-'+fecha+'.json'
    )


#with open('detalleEmpresas.json', 'w') as file:
    #json.dump(detalleEmpresas, file, indent=4)

#import tinys3

#conn = tinys3.Connection('S3_ACCESS_KEY','S3_SECRET_KEY',tls=True)

#f = open('some_file.zip','rb')
#conn.upload('some_file.zip',f,'my_bucket')
