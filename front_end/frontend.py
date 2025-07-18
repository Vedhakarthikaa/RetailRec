import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="RecoStream", layout="centered")
st.title("🛒 Product Recommendation System")

st.markdown("🔍 Enter Customer ID to get personalized or general product recommendations.")
customer_id = st.text_input("Customer ID (e.g., CUST1234)")

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            API_URL = "https://retailrec-api.onrender.com/recommend"  

            response = requests.get(API_URL, params={"customer_id": customer_id})

            data = response.json()

            if not data["data"]:
                st.warning("No recommendations found.")
            else:
                st.success("📦 Recommendations:" if data["type"] == "personalized" else "🌟 Popular Products for All")

                for item in data["data"]:
                    st.markdown(f"""
                        <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;">
                        <strong>🆔 Product ID:</strong> {item['Product ID']}<br>
                        <strong>📂 Category:</strong> {item['Category']}<br>
                        <strong>💰 Price per Unit:</strong> ₹{item['Price per Unit']}<br>
                        <strong>🧮 Times Bought:</strong> {item['Count']}
                        </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
