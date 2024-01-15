

import streamlit as st

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore
from firebase_admin import auth

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()




def main():
    # page configuration 
    st.set_page_config(page_title="OpenAI", page_icon="🖖",layout="wide")
    
    
    
    
    
    
    
    
    




main()



# 