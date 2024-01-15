

import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Assuming you have already set the secrets in Streamlit using st.secrets["your_secret_name"]
service_account_type = st.secrets["type"]
project_id = st.secrets["project_id"]
private_key_id = st.secrets["private_key_id"]
private_key = st.secrets["private_key"]
client_email = st.secrets["client_email"]
client_id = st.secrets["client_id"]
auth_uri = st.secrets["auth_uri"]
token_uri = st.secrets["token_uri"]
auth_provider_x509_cert_url = st.secrets["auth_provider_x509_cert_url"]
client_x509_cert_url = st.secrets["client_x509_cert_url"]
universe_domain = st.secrets["universe_domain"]
p1_n = st.secrets["p1_name"]
p2_n = st.secrets["p2_name"]
p3_n = st.secrets["p3_name"]
p4_n = st.secrets["p4_name"]
p5_n = st.secrets["p5_name"]
p6_n = st.secrets["p6_name"]
# Create a JSON object
json_data = {
    "type": service_account_type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}
# Create a credentials.Certificate object
cred = credentials.Certificate(json_data)
if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

def main():
    # Initialize session state
    if 'date_input' not in st.session_state:
        st.session_state.date_input = datetime.today()
        
    # page configuration 
    st.set_page_config(page_title="OpenAI", page_icon="🖖",layout="wide")
    
    # Streamlit UI
    st.title("Daily Tiffin Expense Tracker")

    # data
    coll_ref_1 = firestore_client.collection("mtrack") 

    # Get today's date
    today_date = st.date_input("Select Date", value= datetime.today())
    
    # Event handler for date input change
    if st.session_state.date_input != today_date:
        st.session_state.date_input = today_date
        
    st.write("----")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    d = coll_ref_1.document(today_date.strftime("%Y-%m-%d")).get().to_dict()

    with col1:
        person1_expense = st.number_input(f"{p1_n}'s Expense", key="person_1_expense",min_value=0,value=(d["p1_expense"] if d else 0),step=10,format="%d")
        person1_settled = st.checkbox(f"Settled",key="person1_settled",value=(d["p1_settled"] if d else False))

    with col2:  
        person2_expense = st.number_input(f"{p2_n}'s Expense", key="person_2_expense",min_value=0,value=(d["p2_expense"] if d else 0),step=10,format="%d")
        person2_settled = st.checkbox(f"Settled",key="person2_settled",value=(d["p2_settled"] if d else False))
    
    with col3:
        person3_expense = st.number_input(f"{p3_n}'s Expense", key="person_3_expense",min_value=0,value=(d["p3_expense"] if d else 0),step=10,format="%d")
        person3_settled = st.checkbox(f"Settled",key="person3_settled",value=(d["p3_settled"] if d else False))
    
    with col4:
        person4_expense = st.number_input(f"{p4_n}'s Expense", key="person_4_expense",min_value=0,value=(d["p4_expense"] if d else 0),step=10,format="%d")
        person4_settled = st.checkbox(f"Settled",key="person4_settled",value=(d["p4_settled"] if d else False))

    with col5:
        person5_expense = st.number_input(f"{p5_n}'s Expense", key="person_5_expense",min_value=0,value=(d["p5_expense"] if d else 0),step=10,format="%d")
        person5_settled = st.checkbox(f"Settled",key="person5_settled",value=(d["p5_settled"] if d else False))
    
    with col6:
        person6_expense = st.number_input(f"{p6_n}'s Expense", key="person_6_expense",min_value=0,value=(d["p6_expense"] if d else 0),step=10,format="%d")
        person6_settled = st.checkbox(f"Settled",key="person6_settled",value=(d["p6_settled"] if d else False))

    # Rest of the code remains the same
    st.write("---")
    


    if st.button("Save Expenses"):
        coll_ref_1.document(today_date.strftime("%Y-%m-%d")).set({
            "date":today_date.strftime("%Y-%m-%d"),
            "p1_expense": person1_expense,
            "p2_expense": person2_expense,
            "p3_expense": person3_expense,
            "p4_expense": person4_expense,
            "p5_expense": person5_expense,
            "p6_expense": person6_expense,
            "p1_settled": person1_settled,
            "p2_settled": person2_settled,
            "p3_settled": person3_settled,
            "p4_settled": person4_settled,
            "p5_settled": person5_settled,
            "p6_settled": person6_settled
        })
        st.success("Expenses saved successfully!")

    def load_expenses_not_settled(l_date,up_date):
        # Get the last month's start and end dates
        l_date = l_date.strftime("%Y-%m-%d")
        up_date = up_date.strftime("%Y-%m-%d")

        # Perform a query to retrieve expenses not settled in the last month
        query = coll_ref_1.where("date", ">=", l_date).where("date", "<=", up_date,use_field_for_ops=True)
        expenses_not_settled = query.stream()

        p1,p2,p3,p4,p5,p6 = 0,0,0,0,0,0
        # Display the sum person-wise for all dates of the last month
        for expense_doc in expenses_not_settled:
            p1+=(expense_doc.get('p1_expense') if expense_doc.get('p1_settled')==False else 0)
            p2+=(expense_doc.get('p2_expense') if expense_doc.get('p2_settled')==False else 0)
            p3+=(expense_doc.get('p3_expense') if expense_doc.get('p3_settled')==False else 0)
            p4+=(expense_doc.get('p4_expense') if expense_doc.get('p4_settled')==False else 0)
            p5+=(expense_doc.get('p5_expense') if expense_doc.get('p5_settled')==False else 0)
            p6+=(expense_doc.get('p6_expense') if expense_doc.get('p6_settled')==False else 0)
        st.write(f"{p1_n}'s Expense: {p1}")
        st.write(f"{p2_n}'s Expense: {p2}")
        st.write(f"{p3_n}'s Expense: {p3}")
        st.write(f"{p4_n}'s Expense: {p4}")
        st.write(f"{p5_n}'s Expense: {p5}")
        st.write(f"{p6_n}'s Expense: {p6}")
        st.write(f"-- Total Expense: {p1+p2+p3+p4+p5+p6}")
    
    st.write("-----")
    l_date,up_date = st.date_input("From Date", value= datetime.today()),st.date_input("To Date", value= datetime.today())
    st.text("Select expenses for dates >= From Date and <= To Date")

    if st.button("Load Expenses"):
        load_expenses_not_settled(l_date,up_date)
        st.success("loaded!")
    
    
    
    
    
    
    




main()



# 