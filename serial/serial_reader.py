import serial
import serial.tools.list_ports
import json
from datetime import datetime
import time
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db import init_db, insert_reading

# Ensure DB exists
init_db()

DEFAULT_BAUD = int(os.getenv("SERIAL_BAUD", "115200"))
ENV_PORT = os.getenv("SERIAL_PORT", "").strip()

def find_port():
    # 1) Use env override if provided
    if ENV_PORT:
        return ENV_PORT

    # 2) Auto-detect common Arduino/USB serial names
    for p in serial.tools.list_ports.comports():
        d = (p.device or "").lower()
        desc = (p.description or "").lower()
        if any(x in d for x in ("usb", "acm", "ttyusb", "ttyacm", "com")) or "arduino" in desc:
            return p.device
    return None

def safe_float(v, default=0.0):
    try:
        return float(v)
    except:
        return default

def run_serial_loop():
    print(f"Starting Serial Reader Service...")
    
    while True:
        port = find_port()
        
        if not port:
            print("⚠️  No Arduino found. Retrying in 2s...")
            time.sleep(2)
            continue
            
        print(f"✅ Attempting to connect to {port} @ {DEFAULT_BAUD}...")
        
        try:
            with serial.Serial(port, DEFAULT_BAUD, timeout=2) as ser:
                print(f"🚀 Connected to {port}!")
                time.sleep(0.5)  # Give Arduino time to initialize
                
                # Clear buffer
                ser.reset_input_buffer()
                
                while True:
                    try:
                        line = ser.readline().decode(errors="ignore").strip()
                        if not line:
                            # No data yet, just loop
                            continue

                        # Expect JSON object per line from Arduino
                        if not (line.startswith("{") and line.endswith("}")):
                            # some boards might send extra text; try to find JSON substring
                            try:
                                start = line.index("{")
                                end = line.rindex("}") + 1
                                line = line[start:end]
                            except Exception:
                                continue

                        try:
                            data = json.loads(line)
                        except Exception:
                            # malformed json - skip
                            continue

                        # Firmware version if provided by the device (optional)
                        firmware = data.get("firmware", None)

                        # Robust conversions
                        temp = safe_float(data.get("temperature", 0.0))
                        humidity = safe_float(data.get("humidity", 0.0))
                        pressure = safe_float(data.get("pressure", 0.0))
                        rain_raw = data.get("rain_value", 0)
                        rain_digital = int(data.get("rain_digital", 1))

                        # Convert raw rain analog to mm using a simple calibration
                        try:
                            rain_raw_f = float(rain_raw)
                        except:
                            rain_raw_f = 0.0

                        if rain_raw_f > 50:
                            # map 0-1023 -> 0-10mm (example)
                            rainfall_mm = round((rain_raw_f / 1023.0) * 10.0, 2)
                        else:
                            rainfall_mm = round(rain_raw_f, 2)

                        status = "Dry" if rain_digital == 1 else "Wet"

                        row = {
                            "timestamp": datetime.now().isoformat(),
                            "temperature_c": temp,
                            "humidity_perc": humidity,
                            "pressure_hpa": pressure,
                            "rainfall_mm": rainfall_mm,
                            "status": status
                        }

                        insert_reading(row)
                        # Minimal console log
                        print(f"[{row['timestamp']}] Inserted: T={temp}C H={humidity}% P={pressure}hPa Rain={rainfall_mm}mm")
                        
                    except serial.SerialException as e:
                        print(f"❌ Serial connection lost: {e}")
                        break # Break inner loop to reconnect
                    except Exception as e:
                        print(f"⚠️ Error processing line: {e}")
                        time.sleep(0.1)
                        
        except Exception as e:
            print(f"❌ Failed to connect to {port}: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        run_serial_loop()
    except KeyboardInterrupt:
        print("Shutting down serial reader.")
