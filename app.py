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
import database as db
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    if username == 'guest':
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('Please logout and log back in')
                
                
        except Exception as e:
            st.error(e)
        #Store user information in Deta
        user_data = {"key": new_username, "name": new_name, "email":new_email, "password": new_password}
        db.db.put(user_data)
        
        authenticator.logout('Logout', 'main', key='unique_key')
        
    else:        
        authenticator.logout('Logout', 'main', key='unique_key')

# if authentication_status:
#     if username == 'guest':
#         try:
#             if authenticator.register_user('Register user', preauthorization=False):
#                     st.write('Please logout and log back in')
                    
#         except Exception as e:
#             st.error(e)
#         with open('config.yaml', 'w') as file:
#                         yaml.dump(config, file, default_flow_style=False)
#         authenticator.logout('Logout', 'main', key='unique_key')
        
#     else:        
#         authenticator.logout('Logout', 'main', key='unique_key')
    
        st.write(f'Welcome *{name}*')
        st.title("Expense Categorization App")
        st.write(f'Your expense.csv should have column names Date, Description, Debit and Credit. "Amount" Column can be used if Debit and Credit columns are not available')
        st.image("expense_example.png", use_column_width=True)
        
        st.write(f'Your category.csv should have the following column names: Keyword and Category. In addition, Keyword-Category pair has to be unique among the list, if duplicated pair/s are identified from the list, this program will run into error')
        st.image("category_example.png", use_column_width=True)
        
        
        def load_category_mapping(file_path):
            category_mapping = {}
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    keyword = row[0].strip().lower()
                    category = row[1].strip()
                    category_mapping[keyword] = category
            return category_mapping


        def categorize_expenses(expenses_file, category_mapping_file):
            category_mapping = load_category_mapping(category_mapping_file)
            categorized_expenses = []

            df = pd.read_csv(expenses_file)
            df.fillna(0, inplace=True)  # Replace NaN values with zero

            header = df.columns.tolist()
            if 'Amount' not in header:
                header.append('Amount')
                has_amount = False
            else:
                has_amount = True

            header.append("Category")
            categorized_expenses.append(header)

            for index, row in df.iterrows():
                description = row['Description'].strip().lower()

                if not has_amount:
                    debit = pd.to_numeric(row['Debit'], errors='coerce')
                    credit = pd.to_numeric(row['Credit'], errors='coerce')
                    amount = debit + credit
                    row['Amount'] = amount

                category_found = False
                for keyword, category in category_mapping.items():
                    if keyword in description:
                        row['Category'] = category
                        categorized_expenses.append(row.tolist())
                        category_found = True
                        break
                if not category_found:
                    row['Category'] = "Uncategorized"
                    categorized_expenses.append(row.tolist())

            return categorized_expenses


        def main():
            
            # YouTube video ID (the string of characters after "v=" in the YouTube URL)
            video_id = "a7yLgMALYtw"
            
            # YouTube embed code
            youtube_embed_code = f"""
            <iframe width="330" height="200" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
            """

            # File upload
            with st.sidebar:
                st.write("## Upload 2 files to get started")
               
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password  \nIf you do not have one, login as guest, passcode is 5566')
