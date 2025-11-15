# serial_reader.py
import serial
import time
import json
import csv
from pathlib import Path

RAW_CSV = Path("raw_data.csv")
SERIAL_PORT = "/dev/ttyUSB0"   # change to your port
BAUDRATE = 115200
RETRY_DELAY = 2.0

HEADERS = ["timestamp","temperature","humidity","pressure","altitude","rain_value","rain_digital"]

def ensure_csv():
    if not RAW_CSV.exists():
        with RAW_CSV.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def append_row(d):
    row = [d.get(h, "") for h in HEADERS]
    with RAW_CSV.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def main():
    ensure_csv()
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=5) as ser:
                print("Connected to", SERIAL_PORT)
                while True:
                    line = ser.readline().decode(errors="ignore").strip()
                    if not line:
                        continue
                    # ignore human readable lines, try parse JSON
                    try:
                        j = json.loads(line)
                        # ensure keys: convert types
                        record = {
                            "timestamp": int(j.get("timestamp", time.time())),
                            "temperature": float(j.get("temperature", 0.0)),
                            "humidity": float(j.get("humidity", 0.0)),
                            "pressure": float(j.get("pressure", 1013.25)),
                            "altitude": float(j.get("altitude", 0.0)),
                            "rain_value": int(j.get("rain_value", 0)),
                            "rain_digital": int(j.get("rain_digital", 1))
                        }
                        append_row(record)
                        print("Appended:", record)
                    except json.JSONDecodeError:
                        # optional: print non-json for debugging
                        print("non-json:", line)
                    except Exception as e:
                        print("parse error:", e, "line:", line)
        except serial.SerialException as e:
            print("Serial error:", e)
            time.sleep(RETRY_DELAY)

if __name__ == "__main__":
    main()
