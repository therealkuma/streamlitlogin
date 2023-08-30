import csv
import pandas as pd
import streamlit as st
import tempfile
import base64
from io import BytesIO
import os
import plotly.express as px
import xlrd
import openpyxl
import plotly.graph_objects as go
import database as jb
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time

df = px.data.iris()

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image:  url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}


[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.write("#### **Expense** **categorization** **app**")

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# --- USER AUTHENTICATION ---

def fetch_users_with_retry():
    max_retries = 3
    retry_delay = 2  # seconds
    retries = 0
    while retries < max_retries:
        try:
            users = jb.fetch_all_users()
            return users
        except Exception as e:
            st.error(f"Error fetching users: {e}")
            retries += 1
            time.sleep(retry_delay)

    st.error("Failed to fetch users after multiple retries.")
    return []

users = fetch_users_with_retry()


# Use the st.cache decorator to cache the result of jb.fetch_all_users()
# @st.cache


# def fetch_users():
#     return jb.fetch_all_users()

# # Call the cached function to fetch users
# users = fetch_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

# Create a JSON format dictionary from the arrays, and then add a top level key call "usernames"
credentials_dict = {
    username: {"name": name, "password": password}
    for username, name, password in zip(usernames, names, hashed_passwords)
}

credentials = {'usernames': credentials_dict}

authenticator = stauth.Authenticate(credentials,
     "sales_dashboard", "abcdef", cookie_expiry_days=30)


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    if username == 'guest':
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('Account created, please logout and log back in')
                
                # access the last username and value of that username's  credentials
                new_username=list(authenticator.credentials['usernames'].keys())[-1]
                last_entry=list(authenticator.credentials['usernames'].values())[-1]
                #st.write(last_entry)
                
                #Store user information in Deta
                new_name = last_entry['name']
                new_password = last_entry['password']
                new_email = last_entry['email']
                user_data = {"key": new_username, "name": new_name, "email": new_email, "password": new_password}
                jb.db.put(user_data)
              
        except Exception as e:
            st.error(e)
        authenticator.logout('Logout', 'main', key='unique_key')
        
    else:        
        authenticator.logout('Logout', 'main', key='unique_key')
    
        st.write(f'Welcome *{name}*')





