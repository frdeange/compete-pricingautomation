import requests
import pandas as pd

# obtener los datos JSON desde la primera URL
response = requests.get('https://cloudbilling.googleapis.com/v2beta/skus?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo&pageSize=5000')

# comprobar si la petición fue exitosa
if response.status_code == 200:
  # convertir los datos JSON en un objeto de Python
  data = response.json()
  # crear una lista vacía para almacenar los resultados
  results = []
  # iterar sobre cada diccionario en la lista data
  for service in data:
    # obtener el skuId del servicio
    skuref = data["skus"]["skuId"]
    # obtener el displayName del servicio
    displayName = service['displayName']
    # obtener la region del servicio
    region = ', '.join(service['serviceRegions']) # unir todas las regiones por servicio con una coma
    
    # hacer otra llamada al otro endpoint para obtener el precio del servicio en euros
    price_url = f'https://cloudbilling.googleapis.com/v1beta/skus/{skuref}/price?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo&currencyCode=EUR'
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
      print(f'Error al obtener el precio del servicio {skuId}')
      price = None
    # crear un diccionario con la información extraída
    result = {
      'skuId': skuref,
      'displayName': displayName,
      'region': region,
      'price': price
    }
    # añadir el diccionario a la lista de resultados
    results.append(result)
  # crear un DataFrame con los resultados
  df = pd.DataFrame(results)
  # guardar el DataFrame como un archivo Excel
  df.to_excel('resultado.xlsx')
else:
  # imprimir un mensaje de error
  print('Error al obtener los datos')