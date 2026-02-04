# main.py
import streamlit as st
from auth import is_authenticated, login, logout

st.set_page_config(page_title="Money Manager", layout="wide")

# Check if user is authenticated
if not is_authenticated():
    # Show login page
    st.title("🔐 Aurenza Money Manager - Login")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Founder Access")
        st.markdown("Enter the shared founder password to access the system.")
        
        with st.form("login_form"):
            password = st.text_input("Password", type="password", placeholder="Enter founder password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if password:
                    if login(password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid password. Please try again.")
                else:
                    st.warning("⚠️ Please enter the password.")
        
        st.markdown("---")
        st.info("💡 **Note**: All 5 founders share the same password for access.")

else:
    # User is authenticated - show Dashboard
    import pandas as pd
    import plotly.express as px
    from db import collection
    
    st.title("Aurenza Money Manager")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Dashboard")
    with col2:
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    # Fetch and display dashboard data
    data = list(collection.find())
    if not data:
        st.info("No transactions yet.")
    else:
        df = pd.DataFrame(data)
        
        # Calculate metrics
        total_income = df[df["type"] == "Income"]["amount"].sum()
        total_expense = df[df["type"] == "Expense"]["amount"].sum()
        balance = total_income - total_expense
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Income", f"₹{total_income:,.0f}")
        col2.metric("Expense", f"₹{total_expense:,.0f}")
        col3.metric("Balance", f"₹{balance:,.0f}")
        
        # Pie chart for category breakdown
        if "tags" in df.columns:
            # Handle tags (multiselect) - flatten the list of tags
            tag_amounts = []
            for _, row in df.iterrows():
                if row.get("tags"):
                    for tag in row["tags"]:
                        tag_amounts.append({"tag": tag, "amount": row["amount"]})
            
            if tag_amounts:
                tag_df = pd.DataFrame(tag_amounts)
                tag_summary = tag_df.groupby("tag")["amount"].sum().reset_index()
                fig = px.pie(tag_summary, names="tag", values="amount", title="By Tags")
                st.plotly_chart(fig, use_container_width=True)
        elif "category" in df.columns:
            fig = px.pie(df, names="category", values="amount", title="By Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Transaction history
        st.subheader("Transaction History")
        
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d-%m-%Y")
        
        def highlight_rows(row):
            if row["type"] == "Expense":
                return ["background-color: #ffcccc"] * len(row)
            else:
                return ["background-color: #ccffcc"] * len(row)
        
        # Prepare columns for display
        display_columns = ["date", "title"]
        if "tags" in df.columns:
            # Convert tags list to string for display
            df["tags_display"] = df["tags"].apply(lambda x: ", ".join(x) if x else "")
            display_columns.append("tags_display")
        elif "category" in df.columns:
            display_columns.append("category")
        
        display_columns.extend(["payment", "type", "amount"])
        
        styled_df = (
            df[display_columns]
            .sort_values(by="date", ascending=False)
            .style.apply(highlight_rows, axis=1)
            .format({"amount": "₹{:,.0f}"})
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
