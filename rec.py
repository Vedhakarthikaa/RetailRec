import streamlit as st
import pandas as pd


order_info = pd.read_csv("order_info.csv")
order_line = pd.read_csv("order_line.csv")
merged = pd.merge(order_info, order_line, on="Order ID")

st.title(" Product Recommendation App")


customer_id = st.text_input("Enter Customer ID (e.g., CUST966)")

if customer_id:
    customer_data = merged[merged["Customer ID"] == customer_id]

    if customer_data.empty:
        st.error("Customer not found.")
    else:
        top_products = (
            customer_data["Product ID"]
            .value_counts()
            .head(3)
            .index
            .tolist()
        )
        st.success(f"Top 3 Products for {customer_id}:")
        st.write(top_products)
