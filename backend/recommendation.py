import pandas as pd


order_info = pd.read_csv("order_info.csv")
order_line = pd.read_csv("order_line.csv")
merged = pd.merge(order_info, order_line, on="Order ID")

def get_customer_recommendations(customer_id):
    customer_orders = merged[merged["Customer ID"] == customer_id]
    if customer_orders.empty:
        return None

    customer_products = customer_orders["Product ID"].unique().tolist()

    relevant_orders = merged[merged["Product ID"].isin(customer_products)]
    related_customers = relevant_orders["Customer ID"].unique()

    peer_data = merged[merged["Customer ID"].isin(related_customers)]
    new_recos = peer_data[~peer_data["Product ID"].isin(customer_products)]

    recos = (
        new_recos.groupby(["Product ID", "Category", "Price per Unit"])
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
        .head(5)
    )
    return recos

def get_general_recommendations():
    return (
        merged.groupby(["Product ID", "Category", "Price per Unit"])
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
        .head(5)
    )
