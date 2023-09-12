# Importar las librerías necesarias
import requests
import pandas as pd
from datetime import datetime


# Obtener el JSON desde la URL
url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/eu-south-2/index.json"
response = requests.get(url)
data = response.json()

# Crear una lista vacía para almacenar los datos de interés
rows = []

# Guardamos la fecha del fichero como un objeto fecha para poder jugar luego con los nombres de fichero
publishDate = datetime.strptime(data["publicationDate"],"%Y-%m-%dT%H:%M:%SZ")

# Recorrer los productos del JSON
for product in data["products"].values():
    # Filtrar solo los productos que tienen atributos de vcpu, memory y storage
    if "vcpu" in product["attributes"] and "memory" in product["attributes"] and "storage" in product["attributes"] and "instanceType" in product["attributes"]:
        # Obtener el sku, instanceType, vcpu, memory y storage del producto
        sku = product["sku"]
        instance = product["attributes"]["instanceType"]
        vcpu = product["attributes"]["vcpu"]
        memory = product["attributes"]["memory"]
        storage = product["attributes"]["storage"]

        # Buscar el precio por unidad del producto en los términos de oferta
        pricePerUnit = None
        # Comprobar si la clave existe antes de acceder a ella
        if sku in data["terms"]["OnDemand"]:
            for term in data["terms"]["OnDemand"][sku].values():
                pricePerUnit = list(term["priceDimensions"].values())[0]["pricePerUnit"]["USD"]
                PriceDescription = list(term["priceDimensions"].values())[0]["description"]

        # Añadir una fila con los datos del producto a la lista
        rows.append([sku, instance, vcpu, memory, storage, PriceDescription, pricePerUnit])

# Crear un dataframe de pandas con la lista de filas y las columnas deseadas
df = pd.DataFrame(rows, columns=["sku", "instanceType", "vcpu", "memory", "storage", "PriceDescription", "pricePerUnit"])

## Convertir el dataframe en un archivo excel y guardarlo. Le añadimos la fecha de actualización del fichero que guardamos al principio.
#filename = "AWS EC2 Spain Prices " + str(publishDate.year) + str(publishDate.month) + str(publishDate.day) + ".xlsx"
filename = "AWS EC2 Spain Prices.xlsx"
df.to_excel(filename, index=False)