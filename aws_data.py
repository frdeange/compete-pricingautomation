import requests
import pandas as pd
from datetime import datetime

def get_aws_data(aws_regions,df):
    # # Create an empty dataframe to store the data
    # df = pd.DataFrame()

    # Request data from AWS for each region
    for aws_region in aws_regions:
        print(aws_region)

        # url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/eu-south-2/index.json"
        # Concatenate the url with the region we want to get the data from
        url = (
            "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/"
            + aws_region
            + "/index.json"
        )

        print(url)

        # Make the call to the API
        response = requests.get(url)

        # Convert the response to a JSON object
        data = response.json()

        # Create an empty list to store the rows of the dataframe
        rows = []

        # Save the date of the last update of the data
        publishDate = datetime.strptime(data["publicationDate"], "%Y-%m-%dT%H:%M:%SZ")

        # Iterate over the products
        for product in data["products"].values():
            # Check if the product has the attributes we want
            if (
                "vcpu" in product["attributes"]
                and "memory" in product["attributes"]
                and "storage" in product["attributes"]
                and "instanceType" in product["attributes"]
            ):
                # Get the values of the attributes we want
                sku = product["sku"]
                instance = product["attributes"]["instanceType"]
                vcpu = product["attributes"]["vcpu"]
                memory = product["attributes"]["memory"]
                storage = product["attributes"]["storage"]

                # Search for the price of the product
                pricePerUnit = None
                # Check if the key exists before accessing it
                if sku in data["terms"]["OnDemand"]:
                    for term in data["terms"]["OnDemand"][sku].values():
                        pricePerUnit = list(term["priceDimensions"].values())[0][
                            "pricePerUnit"
                        ]["USD"]
                        PriceDescription = list(term["priceDimensions"].values())[0][
                            "description"
                        ]

                # Adding a row with product data to the list
                rows.append(
                    [
                        aws_region,
                        sku,
                        instance,
                        vcpu,
                        memory,
                        storage,
                        PriceDescription,
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
                        "vcpu",
                        "memory",
                        "storage",
                        "PriceDescription",
                        "pricePerUnit",
                    ],
                ),
            ],
            ignore_index=True,
        )

    return df