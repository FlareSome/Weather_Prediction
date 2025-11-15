import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_model():

    df = pd.read_csv("raw_data.csv")

    # Print columns so user can see actual names
    print("Detected CSV Columns:", list(df.columns))

    # Try to auto-map column names (fixes your error)
    col_map = {
        "temperature": ["temperature", "temperature_c", "temp"],
        "humidity": ["humidity", "humidity_perc", "hum"],
        "pressure": ["pressure", "pressure_hpa"],
        "rain_value": ["rain_value", "rainfall_mm", "rain"],
    }

    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        raise KeyError(f"None of these columns were found: {possible_names}")

    temp_col = find_col(col_map["temperature"])
    hum_col = find_col(col_map["humidity"])
    pres_col = find_col(col_map["pressure"])
    rain_col = find_col(col_map["rain_value"])

    # Map to unified names
    df = df.rename(columns={
        temp_col: "temperature",
        hum_col: "humidity",
        pres_col: "pressure",
        rain_col: "rain_value",
    })

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df = df.sort_values("timestamp")

    # Feature engineering
    df["hour"] = df["timestamp"].dt.hour
    df["dayofyear"] = df["timestamp"].dt.dayofyear

    features = ["temperature", "humidity", "pressure", "rain_value", "hour", "dayofyear"]
    target = "temperature"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(n_estimators=200)
    model.fit(X_train, y_train)

    joblib.dump(model, "temp_forecast_model.pkl")
    print("Model saved: temp_forecast_model.pkl")

if __name__ == "__main__":
    train_model()
