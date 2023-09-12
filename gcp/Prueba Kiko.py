import requests
import pandas as pd
import json

# obtener los datos JSON desde la primera URL
response = requests.get('https://cloudbilling.googleapis.com/v2beta/skus?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo&pageSize=5000')

# convertir los datos JSON en un objeto de Python
data = response.json()

# crear una lista vacía para almacenar los resultados
rows = []

# Recorrer los productos del JSON
for skus in data["skus"]:
    # Obtener el sku, instanceType, vcpu, memory y storage del producto
    skuid = skus["skuId"]
    displayName = skus["displayName"]
    if "regionalMetadata" in skus["geoTaxonomy"]:
        region = skus["geoTaxonomy"]["regionalMetadata"]["region"]["region"]
    else: region = ""

    price_url = f'https://cloudbilling.googleapis.com/v1beta/skus/{skuid}/price?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo?currencyCode=EUR'
    price_response = requests.get(price_url)
    # comprobar si la petición fue exitosa
    if price_response.status_code == 200:
      # convertir los datos JSON en un objeto de Python
      price_data = price_response.json()
      # obtener la unidad y los nanos del precio
      unit = price_data['pricingExpression']['tieredRates'][0]['unitPrice']['units']
      nanos = price_data['pricingExpression']['tieredRates'][0]['unitPrice']['nanos']
      # convertir los nanos a una fracción decimal
      fraction = nanos / (10 ** 9)
      # sumar la unidad y la fracción para obtener el precio total
      price = unit + fraction
    else:
      # imprimir un mensaje de error y asignar un valor nulo al precio
      print(f'Error al obtener el precio del servicio {skuid}')
      price = None

    rows.append([skuid, displayName, region, price])

df = pd.DataFrame(rows, columns=["skuid", "displayName", "region", "price"])
    
filename = "Prueba Pricing Kiko.xlsx"
df.to_excel(filename, index=False)