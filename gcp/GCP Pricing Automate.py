import requests
import pandas as pd

# Define la URL de la API y el token de autenticación
url = "https://cloudbilling.googleapis.com/v2beta/skus?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo&pageSize=5000"


# Crea una lista vacía para almacenar los skus
skus = []

# Inicializa el nextPageToken con un valor cualquiera
nextPageToken = ""

# Haz un bucle mientras haya un nextPageToken
while nextPageToken:
    # Añade el token a los parámetros de la URL
    params = {"PageToken": nextPageToken}
    # Haz la petición a la API
    response = requests.get(url, params=params)

    # Convierte la respuesta en un diccionario
    data = response.json()
    
    # Extrae la lista de skus y el nextPageToken del diccionario
    skus_list = data["skus"]
    nextPageToken = data["nextPageToken"]
    
    # Añade la lista de skus a la lista general
    skus.extend(skus_list)

# Crea un dataframe con la lista de skus
df = pd.DataFrame(skus)

# Guarda el dataframe en un fichero excel
df.to_excel("GCP Pricing.xlsx")