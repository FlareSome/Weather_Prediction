# api/latest_sensor.py (replace get_latest_sensor)
from fastapi import APIRouter
import sqlite3
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "weather_data.db")

def get_latest_sensor():
    """Return the latest IoT sensor reading from SQLite (safe & compatible with DB schema)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # 'readings' table exists in db/db.py schema
        cur.execute("""
            SELECT timestamp, temperature_c, humidity_perc, pressure_hpa, rainfall_mm, status
            FROM readings
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        # Freshness check: if older than 30 mins, treat as disconnected
        from datetime import datetime, timedelta
        
        # Parse timestamp (assuming ISO format as per db.py)
        try:
            ts_str = row[0]
            reading_time = datetime.fromisoformat(ts_str)
            # If older than 5 seconds, treat as disconnected (sensor sends data every ~0.2s)
            if datetime.now() - reading_time > timedelta(seconds=5):
                # Data is stale
                return None
        except Exception as e:
            print("Timestamp parse error:", e)
            # If we can't parse time, assume it's valid or let it pass? 
            # Safer to return None if we can't verify freshness
            return None

        return {
            "timestamp": row[0],
            "temperature_c": row[1],
            "humidity_perc": row[2],
            "pressure_hpa": row[3],
            # original code used wind_speed_kph — not available in this schema; set None
            "wind_speed_kph": None,
            "rainfall_mm": row[4],
            "status": row[5],
        }
    except Exception as e:
        print("Sensor DB error:", e)
        return None


@router.get("/latest")
def api_latest():
    return get_latest_sensor() or {"error": "No sensor data"}
