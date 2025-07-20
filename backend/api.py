from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow CORS so Streamlit frontend can call backend (important for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return recos.to_dict(orient="records")

def get_general_recommendations():
    recos = (
        merged.groupby(["Product ID", "Category", "Price per Unit"])
        .size()
        .reset_index(name="Count")
        .sort_values(by="Count", ascending=False)
        .head(5)
    )
    return recos.to_dict(orient="records")

@app.get("/recommend")
def recommend(customer_id: str = Query(None)):
    if customer_id:
        data = get_customer_recommendations(customer_id)
        if not data:
            return {"type": "personalized", "data": []}
        return {"type": "personalized", "data": data}
    data = get_general_recommendations()
    return {"type": "general", "data": data}
