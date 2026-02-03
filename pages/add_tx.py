import streamlit as st
from db import collection
from datetime import datetime

st.header("Add Transaction")

with st.form("add_tx"):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Title")
        amount = st.number_input("Amount", min_value=0.0)
        category = st.selectbox("Category", ["Sales", "Expense", "Salary", "Office"])
        tx_date = st.date_input("Transaction Date")

    with col2:
        payment = st.selectbox("Payment Mode", ["Cash", "Card", "UPI", "Bank"])
        tx_type = st.radio("Type", ["Income", "Expense"])

    submit = st.form_submit_button("Add Transaction")

    if submit:
        collection.insert_one({
            "title": title,
            "amount": amount,
            "category": category,
            "payment": payment,
            "type": tx_type,
            "date": datetime.combine(tx_date, datetime.min.time())
        })
        st.success("Transaction added!")
