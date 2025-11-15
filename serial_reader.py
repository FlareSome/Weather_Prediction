import serial
import json
import pandas as pd
from datetime import datetime

CSV_FILE = "raw_data.csv"

# Ensure CSV has correct headers
columns = [
    "timestamp",
    "temperature_c",
    "humidity_perc",
    "pressure_hpa",
    "rainfall_mm",
    "status"     # Dry/Wet
]

# Create CSV if missing
try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=columns)
    df.to_csv(CSV_FILE, index=False)

print("Listening on /dev/ttyACM0 ...")
ser = serial.Serial("/dev/ttyACM0", 115200)

while True:
    try:
        line = ser.readline().decode().strip()
        if not line.startswith("{"):
            continue

        data = json.loads(line)

        # Convert Arduino fields → CSV fields
        entry = {
            "timestamp": datetime.now().isoformat(),
            "temperature_c": float(data.get("temperature", 0)),
            "humidity_perc": float(data.get("humidity", 0)),
            "pressure_hpa": float(data.get("pressure", 0)),
            "rainfall_mm": float(data.get("rain_value", 0) / 10.0),  # simple scaling
            "status": "Dry" if data.get("rain_digital", 1) == 1 else "Wet"
        }

        # Append to CSV
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        print("Saved:", entry)

    except Exception as e:
        print("Error:", e)
