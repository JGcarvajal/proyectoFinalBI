import requests
import json
from os import remove
import boto3

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

#empresas=["IBM","EPM","EC","CIB"]
empresas=["EC"]

#Al consultar en la aplicancion el endpoint Query se
#extrae la informacion necesaria y se adiciona a los
#documentos.

detalleEmpresas=[]
gananciasAnuales=[]
banlancesAnuales=[]
historicos=[]
cambioMoneda=[]

#Creamos el cliente de S3
#s3_client=boto3.client('s3',aws_access_key_id='AKIAZKHZZ4X2LRKJVJHB',aws_secret_access_key="")
s3_client=boto3.client('s3')

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


#Historico de tasa de cambio de dolar a peso colombiano cada 5 min
reqcambio = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=COP&interval=5min&apikey=55A5SUC3FX5Y4F6N&datatype=json&outputsize=full')
reqStatus=reqcambio.status_code
if reqStatus==200:
    cambioMoneda.append(reqcambio.json())

#enviamos los archivos a S3
s3_client.put_object(Body=detalleEmpresas,Bucket='proyecto-final-bi-jgc-jac', Key='apy_alphavantage/detalle_empresas/detalleEmpresas.json' )

#Borramos lso archivos para evitar mesclar los datos
#remove("detalleEmpresas.json")
#remove("gananciasAnuales.json")
#remove("banlancesAnuales.json")
#remove("historicos.json")
#remove("cambioMoneda.json")

#with open('detalleEmpresas.json', 'w') as file:
    #json.dump(detalleEmpresas, file, indent=4)

#with open('gananciasAnuales.json', 'w') as file:
    #json.dump(gananciasAnuales, file, indent=4)

#with open('banlancesAnuales.json', 'w') as file:
   # json.dump(banlancesAnuales, file, indent=4)

#with open('historicos.json', 'w') as file:
    #json.dump(historicos, file, indent=4)

#with open('cambioMoneda.json', 'w') as file:
    #json.dump(cambioMoneda, file, indent=4)

#import tinys3

#conn = tinys3.Connection('S3_ACCESS_KEY','S3_SECRET_KEY',tls=True)

#f = open('some_file.zip','rb')
#conn.upload('some_file.zip',f,'my_bucket')
