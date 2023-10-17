import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from aws_data import get_aws_data
from azure_data import get_azure_data


st.title("VMs prices across clouds")


########################## Sidebar configuration ##########################
# Sidebar para seleccionar las instancias que queremos consultar
st.sidebar.header("Select the type of VM you want to compare")
st.sidebar.subheader("Instance Type")
instanceType = st.sidebar.multiselect("Select the instance type", ["a1", "c5d.xlarge"])

st.sidebar.subheader("Price Description")
priceDescription = st.sidebar.multiselect(
    "Select the price description",
    [
        "Dedicated Reservation Linux",
        "Dedicated Reservation Windows",
        "Dedicated Reservation Linux with SQL Server Enterprise",
    ],
)


########################## Get data ##########################


# Regions we want to get the data from
aws_regions = ["eu-south-2", "eu-west-1"]
azure_regions = ["EU West"]

# Create empty dataframe
df = pd.DataFrame(
    #     columns=[
    #         "region",
    #         "sku",
    #         "instanceType",
    #         "vcpu",
    #         "memory",
    #         "storage",
    #         "PriceDescription",
    #         "pricePerUnit",
    #     ]
)

aws_df = get_aws_data(aws_regions, df)
azure_df = get_azure_data(azure_regions, df)


st.caption("AWS")
# If no instance has been selected, paint the complete dataframe
if not instanceType:
    st.dataframe(aws_df)
else:
    # Paint the dataframe filtered by the selected instances and WHERE A PARTIAL STRING of the price description is in the priceDescription array
    st.dataframe(
        aws_df[
            aws_df["instanceType"].isin(instanceType)
            & aws_df["PriceDescription"].str.contains("|".join(priceDescription))
        ]
    )

# A new dataframe for azure
# azure_df = get_azure_data(azure_regions, df)
st.caption("Azure")
st.dataframe(azure_df)

# Añadir un botón para descargar el dataframe como un archivo excel
# st.download_button(
#     label="Download data as Excel",
#     data=df.to_excel().encode("utf-8"),
#     file_name='AWS EC2 Spain Prices.csv',
# )

# dataframe with width expanded
# st.dataframe(df.style.set_table_attributes("style='display:inline'").set_caption('Caption table'))
