import requests
import pandas as pd
from datetime import datetime

def get_azure_data(azure_regions,df):
  
    # Request data from AWS for each region
    for azure_region in azure_regions:
        print(azure_region)


        # Make the call to the API
        response = requests.get("https://prices.azure.com/api/retail/prices?currencyCode='EUR'&$filter=serviceName eq 'Virtual Machines' and Location eq 'EU West' and PriceType eq 'Consumption'")
        
        # Convert the response to a JSON object
        data = response.json()

        print(data)

        # Create an empty list to store the rows of the dataframe
        rows = []

        #
        print(data["Items"])
       
        # Iterate over the products
        # for product in data["Items"].values():
        for product in data["Items"]:
            # Check if the product has the attributes we want
            # if (
            #     # "vcpu" in product["attributes"]
            #     and "memory" in product["attributes"]
            #     and "storage" in product["attributes"]
            #     and "skuName" in product["attributes"]
            # ):
                # Get the values of the attributes we want
                sku = product["skuName"]
                instance = product["armSkuName"]
                # vcpu = product["attributes"]["vcpu"]
                # memory = product["attributes"]["memory"]
                # storage = product["attributes"]["storage"]

                # Search for the price of the product
                pricePerUnit = product["retailPrice"]
                # Check if the key exists before accessing it
                # if sku in data["terms"]["OnDemand"]:
                #     for term in data["terms"]["OnDemand"][sku].values():
                #         pricePerUnit = list(term["priceDimensions"].values())[0][
                #             "pricePerUnit"
                #         ]["USD"]
                #         PriceDescription = list(term["priceDimensions"].values())[0][
                #             "description"
                #         ]



                # Adding a row with product data to the list
                # rows.append(
                #     [
                #         aws_region,
                #         sku,
                #         instance,
                #         vcpu,
                #         memory,
                #         storage,
                #         PriceDescription,
                #         pricePerUnit,
                #     ]
                # )
                rows.append(
                    [
                        azure_region,
                        sku,
                        instance,
                        # vcpu,
                        # memory,
                        # storage,
                        # PriceDescription,
                        pricePerUnit,
                    ]
                )

        # Make an append of the data for each region
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    rows,
                    columns=[
                        "region",
                        "sku",
                        "instanceType",
                        # "vcpu",
                        # "memory",
                        # "storage",
                        # "PriceDescription",
                        "pricePerUnit",
                    ],
                ),
            ],
            ignore_index=True,
        )

    return df