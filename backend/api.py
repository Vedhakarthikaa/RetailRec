from fastapi import FastAPI
from backend.recommendation import get_customer_recommendations, get_general_recommendations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to RetailRec API"}

@app.get("/recommend")
def recommend(customer_id: str):
    result = get_customer_recommendations(customer_id)
    if result is None or result.empty:
        return {"type": "general", "data": get_general_recommendations().to_dict(orient="records")}
    return {"type": "personalized", "data": result.to_dict(orient="records")}
