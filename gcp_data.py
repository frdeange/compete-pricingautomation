import requests
import pandas as pd
from datetime import datetime

import requests
import json

def get_gcp_data(gcp_regions):
    # Create an empty list to store the data
    data = []

    # Request data from GCP for each region
    for gcp_region in gcp_regions:
        print(gcp_region)

        # Make the call to the API
        response = requests.get(f"https://cloudbilling.googleapis.com/v2beta/skus?key=AIzaSyCy-LbDhf8DcyNQIGmFHq3_Za_aM_ML4fo&pageSize=5000")
        
        # Convert the response to a JSON object
        json_data = response.json()

        # Iterate over the products
        for product in json_data["gcp_price_list"]:
            # Check if the product has the attributes we want
            if (
                "cores" in product
                and "memory" in product
                and "disk" in product
                and "name" in product
                and "region" in product
            ):
                # Get the values of the attributes we want
                sku = product["name"]
                instance = product["name"]
                vcpu = product["cores"]
                memory = product["memory"]
                storage = product["disk"]
                region = product["region"]

                # Search for the price of the product
                pricePerUnit = None
                for pricing_info in product["pricing_info"]:
                    if pricing_info["unit"] == "1h":
                        pricePerUnit = pricing_info["price"]

                # Adding a dictionary with product data to the list
                data.append(
                    {
                        "region": region,
                        "sku": sku,
                        "instanceType": instance,
                        "vcpu": vcpu,
                        "memory": memory,
                        "storage": storage,
                        "pricePerUnit": pricePerUnit,
                    }
                )

    # Convert the list of dictionaries to a JSON object
    json_data = json.dumps(data)



    return json_data