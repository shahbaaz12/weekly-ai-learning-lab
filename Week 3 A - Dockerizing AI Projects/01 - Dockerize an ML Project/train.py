# What this file does: trains a small delivery-time model and saves it for the API.

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


np.random.seed(42)
rows = 1000

data = pd.DataFrame(
    {
        "distance_km": np.random.uniform(0.5, 12, rows),
        "prep_time_min": np.random.uniform(5, 30, rows),
        "rider_available": np.random.randint(0, 2, rows),
        "is_raining": np.random.randint(0, 2, rows),
    }
)

data["eta_min"] = (
    8
    + data.distance_km * 3
    + data.prep_time_min * 0.7
    + data.is_raining * 9
    + (1 - data.rider_available) * 6
)

features = data.drop(columns=["eta_min"])
target = data["eta_min"]
model = RandomForestRegressor(n_estimators=30, random_state=42).fit(features, target)

joblib.dump(model, "eta_model.pkl")
print("Model saved: eta_model.pkl")
