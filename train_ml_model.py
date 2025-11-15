import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

DATA_FILE = "raw_data.csv"
MODEL_FILE = "ml_weather_model.pkl"

print("Loading dataset:", DATA_FILE)

if not os.path.exists(DATA_FILE):
    print("ERROR: CSV file not found!")
    exit()

df = pd.read_csv(DATA_FILE)

if df.empty:
    print("ERROR: CSV file is EMPTY!")
    exit()

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

# Required numeric columns
required_cols = ["temperature_c", "humidity_perc", "pressure_hpa", "rainfall_mm"]

for c in required_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=required_cols)

# Create time-based features
df["hour"] = df["timestamp"].dt.hour
df["dayofyear"] = df["timestamp"].dt.dayofyear

FEATURES = ["temperature_c", "humidity_perc", "pressure_hpa", "rainfall_mm", "hour", "dayofyear"]

print("Training with features:", FEATURES)

X = df[FEATURES]
y = df["temperature_c"]     # Predict future temperature from past temperature

model = RandomForestRegressor(
    n_estimators=400,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

joblib.dump(model, MODEL_FILE)

print("\n🎉 Model training complete!")
print("Saved model to:", MODEL_FILE)
print("\nModel expects features:", list(model.feature_names_in_))
