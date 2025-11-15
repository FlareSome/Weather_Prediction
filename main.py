# main.py — Live Streamlit dashboard with auto-train fallback
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import time
from datetime import datetime, timedelta

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ---------- CONFIG ----------
CSV_PATH = "raw_data.csv"
MODEL_PATH = "trained_weather_model.pkl"
AUTO_REFRESH_SECONDS = 5
MIN_ROWS_TO_TRAIN = 30   # require at least this many rows to auto-train

st.set_page_config(page_title="Smart Weather Dashboard", layout="wide")
st.title("🌦 Smart Weather Dashboard (Live IoT + ML)")
st.write("Automatically updating every few seconds...")

# ---------- Helper functions ----------
def safe_load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    if df.empty:
        return df
    # convert types and drop bad rows
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for col in ["temperature_c", "humidity_perc", "pressure_hpa", "rainfall_mm"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["timestamp", "temperature_c", "humidity_perc", "pressure_hpa", "rainfall_mm"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def prepare_training_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features and target. Target is next-row temperature (next sample's temperature)
    We'll compute simple features from each row and shift -1 to be the target.
    """
    t = df.copy()
    # add day-of-year for seasonality
    t["dayofyear"] = t["timestamp"].dt.dayofyear
    # features we will use
    features = ["temperature_c", "humidity_perc", "pressure_hpa", "rainfall_mm", "dayofyear"]
    # target is next sample's temperature (shifted up)
    t["target_next_temp"] = t["temperature_c"].shift(-1)
    t = t.dropna(subset=features + ["target_next_temp"])
    return t, features, "target_next_temp"

def train_and_save_model(df: pd.DataFrame, model_path: str) -> object:
    t, features, target = prepare_training_df(df)
    if len(t) < MIN_ROWS_TO_TRAIN:
        raise ValueError(f"Not enough rows to train: {len(t)} < {MIN_ROWS_TO_TRAIN}")
    X = t[features]
    y = t[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    # save
    joblib.dump({"model": model, "features": features}, model_path)
    return {"model": model, "features": features}

def load_model_or_train(df: pd.DataFrame, model_path: str):
    # Try load
    if os.path.exists(model_path):
        try:
            payload = joblib.load(model_path)
            # payload should be dict {"model":..., "features":[...]}
            if isinstance(payload, dict) and "model" in payload and "features" in payload:
                return payload
        except Exception as e:
            st.warning(f"Failed to load existing model: {e}. Will attempt retrain.")
    # If reach here, attempt training if enough data
    try:
        payload = train_and_save_model(df, model_path)
        st.success("Trained new ML model from CSV and saved to disk.")
        return payload
    except Exception as e:
        st.error(f"No ML model available and training failed: {e}")
        return None

def make_7day_forecast(model_payload, latest_row):
    """
    Build 7 rows of inputs using latest reading as baseline.
    The model expects exact feature names present in model_payload['features'].
    """
    features = model_payload["features"]
    model = model_payload["model"]

    # build future dataframe
    base_day = int(latest_row["timestamp"].dayofyear)
    inputs = []
    for i in range(1, 8):
        di = {}
        # map feature names: if dayofyear present compute, else set reasonable guess
        for f in features:
            if f == "dayofyear":
                di[f] = base_day + i
            elif f == "temperature_c":
                di[f] = latest_row["temperature_c"]
            elif f == "humidity_perc":
                di[f] = latest_row["humidity_perc"]
            elif f == "pressure_hpa":
                di[f] = latest_row["pressure_hpa"]
            elif f == "rainfall_mm":
                di[f] = latest_row["rainfall_mm"]
            else:
                # unknown feature: try to find in latest_row or set 0
                di[f] = latest_row.get(f, 0)
        inputs.append(di)
    X_future = pd.DataFrame(inputs)[features]
    preds = model.predict(X_future)
    return preds

# ---------- Load data ----------
df = safe_load_csv(CSV_PATH)
if df.empty:
    st.warning("⏳ Waiting for sensor data (raw_data.csv is missing or empty). Start serial_reader.py and wait a few readings.")
    # place auto-refresh at end
    st.toast(f"🔄 Auto-refresh in {AUTO_REFRESH_SECONDS}s...")
    time.sleep(AUTO_REFRESH_SECONDS)
    st.rerun()

# ---------- Show latest reading ----------
latest = df.iloc[-1]
st.subheader("📡 Latest IoT Sensor Reading")
col1, col2, col3 = st.columns(3)
col1.metric("🌡 Temperature (°C)", f"{latest['temperature_c']:.1f}")
col2.metric("💧 Humidity (%)", f"{latest['humidity_perc']:.1f}")
col3.metric("📊 Pressure (hPa)", f"{latest['pressure_hpa']:.2f}")

col4, col5 = st.columns(2)
col4.metric("🌧 Rain Value", f"{latest['rainfall_mm']:.1f}")
col5.metric("Status", latest.get("status", "N/A"))

st.divider()

# ---------- Load or train model ----------
model_payload = load_model_or_train(df, MODEL_PATH)

if model_payload is None:
    st.warning("ML model not available. Dashboard will still show live sensor data. Fix CSV/model to enable forecasts.")
    # auto-refresh and stop here
    st.toast(f"🔄 Auto-refresh in {AUTO_REFRESH_SECONDS}s...")
    time.sleep(AUTO_REFRESH_SECONDS)
    st.rerun()

# ---------- Forecast ----------
try:
    preds = make_7day_forecast(model_payload, latest)
    forecast_df = pd.DataFrame({
        "Day": [ (latest["timestamp"] + pd.to_timedelta(i, unit="D")).strftime("%Y-%m-%d") for i in range(1,8) ],
        "Predicted Temp (°C)": np.round(preds, 2)
    })
    st.subheader("📅 7-Day Forecast (ML prediction of next-day temperature)")
    st.dataframe(forecast_df, use_container_width=True)
    st.line_chart(forecast_df.set_index("Day")["Predicted Temp (°C)"])
except Exception as e:
    st.error(f"Failed to compute forecast: {e}")

# ---------- Footer / auto-refresh ----------
st.info(f"Dashboard auto-refreshes every {AUTO_REFRESH_SECONDS} seconds.")
time.sleep(AUTO_REFRESH_SECONDS)
st.rerun()
