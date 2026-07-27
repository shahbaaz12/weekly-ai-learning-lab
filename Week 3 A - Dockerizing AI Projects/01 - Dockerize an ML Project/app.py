# What this file does: serves the trained QuickBite ETA model through a FastAPI API.

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="QuickBite ETA")
model = joblib.load("eta_model.pkl")


class Order(BaseModel):
    distance_km: float
    prep_time_min: float
    rider_available: int
    is_raining: int


@app.get("/")
def health():
    return {"status": "QuickBite ETA is live"}


@app.post("/predict")
def predict(order: Order):
    features = pd.DataFrame([order.model_dump()])
    eta = round(float(model.predict(features)[0]), 1)
    return {"eta_minutes": eta, "message": f"Your food arrives in {eta} minutes."}
