import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
API_KEY = os.getenv("WEATHER_API_KEY")

# Simple in-memory cache
_cache_now = {"data": None, "timestamp": 0}
_cache_7day = {"data": None, "timestamp": 0}
CACHE_DURATION = 300  # 5 minutes

def get_weatherapi_now(city="Kolkata"):
    """Fetch current weather from WeatherAPI (cached)."""
    if not API_KEY:
        return None

    import time
    now = time.time()
    if _cache_now["data"] and (now - _cache_now["timestamp"] < CACHE_DURATION):
        return _cache_now["data"]

    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        r = requests.get(url, timeout=10).json()
        c = r["current"]

        data = {
            "current": {
                "temperature_c": c["temp_c"],
                "humidity": c["humidity"],
                "pressure_hpa": c["pressure_mb"],
                "wind_kph": c.get("wind_kph"),
                "feelslike_c": c.get("feelslike_c"),
                "condition": c["condition"]["text"],
                "rainfall_mm": c.get("precip_mm", 0)
            }
        }
        _cache_now["data"] = data
        _cache_now["timestamp"] = now
        return data
    except Exception as e:
        print("WeatherAPI current error:", e)
        return _cache_now["data"] # Return stale data if fetch fails

def get_weatherapi_7day(city="Kolkata"):
    """7-day forecast (cached)."""
    if not API_KEY:
        return None

    import time
    now = time.time()
    if _cache_7day["data"] and (now - _cache_7day["timestamp"] < CACHE_DURATION):
        return _cache_7day["data"]

    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7&aqi=no"
        r = requests.get(url, timeout=10).json()

        data = [
            {
                "day": d["date"],
                "temp_high_c": d["day"]["maxtemp_c"],
                "temp_low_c": d["day"]["mintemp_c"],
                "rain_prob_perc": d["day"].get("daily_chance_of_rain", 0),
                "condition": d["day"]["condition"]["text"],
                "sunrise": d["astro"]["sunrise"],
                "sunset": d["astro"]["sunset"],
            }
            for d in r["forecast"]["forecastday"]
        ]
        _cache_7day["data"] = data
        _cache_7day["timestamp"] = now
        return data
    except Exception as e:
        print("WeatherAPI 7day error:", e)
        return _cache_7day["data"]


@router.get("/weatherapi")
def api_weather_now():
    return get_weatherapi_now() or {"error": "WeatherAPI current unavailable"}


@router.get("/weatherapi_7day")
def api_weather_7day():
    return get_weatherapi_7day() or {"error": "WeatherAPI 7day unavailable"}


# New Sync Endpoint
from datetime import datetime
from db.db import insert_forecast_batch

@router.get("/weatherapi/sync")
def sync_weatherapi():
    """Fetch 7-day forecast and save to DB."""
    data = get_weatherapi_7day()
    if not data:
        return {"status": "error", "message": "Could not fetch data from WeatherAPI"}
    
    try:
        # Insert into DB
        insert_forecast_batch(
            source="WeatherAPI",
            created_at=datetime.now().isoformat(),
            forecast_list=data,
            summary="Manual Sync"
        )
        return {"status": "success", "message": f"Synced {len(data)} days to DB"}
    except Exception as e:
        print("Sync error:", e)
        return {"status": "error", "message": str(e)}
