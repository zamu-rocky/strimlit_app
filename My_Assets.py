####################################################################################
# My Assets App                                                                    #
# Query Assets in ServiceNow (HAM - alm_assets) by User ID using Streamlit as GUI  #
#                                                                                  #
# Author: Luis A. Urso                                                             #
# Version: 1.0                                                                     #
####################################################################################

import requests
import pandas as pd
import json
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os

# Get UserId and Password from .env file

load_dotenv()

ct1 = st.container(border=True)
ct2 = st.container(border=True)

st.logo("lilly_logo.png",size="large")

ct1.title(":red[Retrieves HAM Information]")
ct1.subheader(":blue[Show all your assets]")

user_id=ct2.text_input("Enter Your User ID:")

ct2.write(" ")

url="https://lilly.service-now.com/api/now/table/alm_asset?sysparm_display_value=true&sysparm_exclude_reference_link=true&sysparm_limit=10000&assigned_to="+user_id

user = os.environ.get("user_id")
pwd = os.environ.get("password")

headers = {"Accept":"application/json"}

response = requests.get(url, auth=(user, pwd), headers=headers)

# Response Check for Errors 

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()
else:
    # Dump a piece of the data
    response_loc_dic = response.json()
    outputs = json.dumps(response_loc_dic["result"])

# Iterate the Responses until EOF and creates the Pandas DB with the Assets List Fields to show

model_category=[]
display_name=[]
install_status=[]
created_date=[]

idx=0

try:
    while True:
        
        model_category.append(response_loc_dic['result'][idx]['model_category'])
        display_name.append(response_loc_dic['result'][idx]['model'])
        install_status.append(response_loc_dic['result'][idx]['install_status'])
        created_date.append(response_loc_dic['result'][idx]['sys_created_on'])

        idx+=1
        
except IndexError:
    
    print("<EOL>")

# Creates the dataframe
    
data = {
         "Categoria":model_category,
         "Modelo":display_name,
         "Status":install_status,
         "Created":created_date
}

df_assets = pd.DataFrame(data)

# Show the Dataframe

ct2.metric(label="No. of Rows",value=idx)
ct2.table(df_assets)