import streamlit as st
import pandas as pd
import plotly.express as px
from db import collection

st.header("Dashboard")

data = list(collection.find())
if not data:
    st.info("No transactions yet.")
    st.stop()

df = pd.DataFrame(data)

total_income = df[df["type"] == "Income"]["amount"].sum()
total_expense = df[df["type"] == "Expense"]["amount"].sum()
balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{total_income:,.0f}")
col2.metric("Expense", f"₹{total_expense:,.0f}")
col3.metric("Balance", f"₹{balance:,.0f}")

fig = px.pie(df, names="category", values="amount", title="By Category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Transaction History")

df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")

def highlight_rows(row):
    if row["type"] == "Expense":
        return ["background-color: #ffcccc"] * len(row)
    else:
        return ["background-color: #ccffcc"] * len(row)

styled_df = (
    df[["date", "title", "category", "payment", "type", "amount"]]
    .sort_values(by="date", ascending=False)
    .style.apply(highlight_rows, axis=1)
    .format({"amount": "₹{:,.0f}"})
)

st.dataframe(styled_df, use_container_width=True, height=400)
