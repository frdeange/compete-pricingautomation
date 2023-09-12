# Importamos los módulos necesarios
import requests
import json
import pandas as pd
import openpyxl

# Definimos la función que obtiene una página de datos a partir de un enlace
def get_page(url):
    # Hacemos una petición GET a la API
    response = requests.get(url)
    # Comprobamos si la respuesta es exitosa
    if response.status_code == 200:
        # Convertimos la respuesta en un diccionario de python
        data = response.json()
        # Creamos una tabla de datos con los campos que nos interesan
        table = pd.DataFrame(data["Items"], columns=["currencyCode", "tierMinimumUnits", "reservationTerm", "retailPrice", "unitPrice", "armRegionName", "location", "effectiveStartDate", "effectiveEndDate", "meterId", "meterName", "productId", "skuId", "productName", "skuName", "serviceName", "serviceId", "serviceFamily", "unitOfMeasure", "type", "isPrimaryMeterRegion", "armSkuName"])
        # Obtenemos el campo NextPageLink
        next_page_link = data["NextPageLink"]
        # Devolvemos una lista con la tabla y el enlace a la siguiente página
        return [table, next_page_link]
    else:
        # Si la respuesta no es exitosa, devolvemos un mensaje de error
        return f"Error: {response.status_code}"

# Definimos la función que genera una lista con todas las páginas de datos concatenadas
def get_all_pages(url):
    # Creamos una lista vacía para almacenar las tablas de datos
    tables = []
    # Creamos un bucle para recorrer todas las páginas
    while url is not None:
        # Obtenemos la página actual usando la función get_page
        page = get_page(url)
        # Añadimos la tabla de datos a la lista
        tables.append(page[0])
        # Actualizamos el enlace a la siguiente página
        url = page[1]
    # Devolvemos la lista con todas las tablas
    return tables

# Llamamos a la función get_all_pages con el enlace a la primera página de datos de la API, usando los mismos filtros que usaste en powerQuery
tables = get_all_pages("https://prices.azure.com/api/retail/prices?currencyCode='EUR'&$filter=serviceName eq 'Virtual Machines' and Location eq 'EU West' and PriceType eq 'Consumption'")

# Convertimos la lista de tablas en un dataframe de pandas, usando el método pd.concat
df = pd.concat(tables)

# Reiniciamos el índice del dataframe
df.reset_index(drop=True, inplace=True)

# Guardamos el dataframe de pandas en un fichero excel, usando el método to_excel y el módulo openpyxl
df.to_excel("azure_prices.xlsx", engine="openpyxl")