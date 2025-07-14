import streamlit as st
import pandas as pd


order_info = pd.read_csv("order_info.csv")
order_line = pd.read_csv("order_line.csv")
merged = pd.merge(order_info, order_line, on="Order ID")

st.set_page_config(page_title="RecoStream", layout="centered")
st.title("🛒 Product Recommendation System")


with st.sidebar:
    st.header("📊 Quick EDA Insights")
    st.write(f"👥 Total Customers: `{merged['Customer ID'].nunique()}`")
    st.write(f"🧺 Total Products: `{merged['Product ID'].nunique()}`")
    st.write("📦 Top Categories:")
    st.dataframe(merged["Category"].value_counts().head(5))

    if st.checkbox("Show Top 5 Active Customers"):
        top_customers = merged["Customer ID"].value_counts().head(5).reset_index()
        top_customers.columns = ["Customer ID", "Orders"]
        st.dataframe(top_customers)


customer_id = st.text_input("🔍 Enter Customer ID (e.g., CUST966)")
st.markdown("Recommendations are based on similar customers' purchases.")

if customer_id:
    customer_orders = merged[merged["Customer ID"] == customer_id]
    if customer_orders.empty:
        st.error("❌ Customer ID not found.")
    else:
        st.subheader(" Customer Profile")
        try:
            age = customer_orders["Customer Age"].mode().values[0]
            gender = customer_orders["Customer Gender"].mode().values[0]
            st.markdown(f"- **Age**: {age}")
            st.markdown(f"- **Gender**: {gender}")
        except:
            st.warning("Could not extract age/gender info.")

        customer_products = customer_orders["Product ID"].unique().tolist()

        
        relevant_orders = merged[merged["Product ID"].isin(customer_products)]

     
        related_customers = relevant_orders["Customer ID"].unique()

       
        peer_data = merged[merged["Customer ID"].isin(related_customers)]

        
        new_recos = peer_data[~peer_data["Product ID"].isin(customer_products)]

        if new_recos.empty:
            st.warning("No new product recommendations found.")
        else:
            recos = (
                new_recos.groupby(["Product ID", "Category", "Price per Unit"])
                .size()
                .reset_index(name="Count")
                .sort_values(by="Count", ascending=False)
                .head(5)
            )

            st.success("📌 Customers who bought similar items also bought:")

            for _, row in recos.iterrows():
                st.markdown(f"""
                <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;">
                <strong>🆔 Product ID:</strong> {row['Product ID']}<br>
                <strong>📦 Category:</strong> {row['Category']}<br>
                <strong>💰 Price per Unit:</strong> ₹{row['Price per Unit']}<br>
                <strong>🛍️ Times Bought:</strong> {row['Count']}
                </div>
                """, unsafe_allow_html=True)

            csv = recos[["Product ID", "Category", "Price per Unit", "Count"]].to_csv(index=False)
            st.download_button("📥 Download Recommendations", csv, "similar_customers_recos.csv", "text/csv")
