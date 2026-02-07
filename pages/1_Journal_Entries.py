import streamlit as st
from db import supabase
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import is_authenticated

# Check authentication
if not is_authenticated():
    st.error("🔒 Please log in to access this page.")
    st.info("👈 Go to the main page to log in.")
    st.stop()

st.header("Add Transaction")

with st.form("add_tx"):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Title")
        amount = st.number_input("Amount", min_value=0.0)
        tags = st.multiselect("Tags", ["Salary", "Travel", "Rent","website Domain","website Hosting","website Maintenance","Development"])
        tx_date = st.date_input("Transaction Date")

    with col2:
        payment = st.selectbox("Payment Mode", ["Cash", "Card", "UPI", "Bank"])
        tx_type = st.radio("Type", ["Income", "Expense"])
        image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg", "gif"])

    submit = st.form_submit_button("Add Transaction")

    if submit:
        tx_data = {
            "title": title,
            "amount": float(amount),
            "tags": tags,
            "payment": payment,
            "type": tx_type,
            "date": datetime.combine(tx_date, datetime.min.time()).isoformat()
        }
        
        # Add image if uploaded
        if image is not None:
            tx_data["image"] = image.read()
            tx_data["image_name"] = image.name
        
        try:
            supabase.table("transactions").insert(tx_data).execute()
            st.success("Transaction added!")
        except Exception as e:
            st.error(f"Error adding transaction: {e}")

