import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
# NOTE: In a real environment, you would import serial and use it here.
# import serial 

# Configuration
MOCK_DATA_INTERVAL_MIN = 5
# LOG PATH UPDATED to new file name
DATA_LOG_PATH = '../data/sensor_readings_log.csv' 

# --- REAL-TIME DATA ACQUISITION (MOCK) ---
# Replace this entire function with actual serial reading logic in a real project.
def get_sensor_data(hours=24):
    """
    Mocks reading the serial port and generating the sensor data DataFrame.
    """
    
    # Data is generated fresh every time the cache TTL expires (60s in main.py)
    NUM_READINGS = hours * (60 // MOCK_DATA_INTERVAL_MIN) 

    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    timestamps = [start_time + (end_time - start_time) * i / (NUM_READINGS - 1)
                  for i in range(NUM_READINGS)]
    
    data = []
    
    # Base weather patterns for simulation
    base_temp = 25.0
    base_humidity = 65.0
    base_pressure = 1012.0 # hPa

    # Simulate sensor readings
    temps = base_temp + np.sin(np.linspace(0, 4*np.pi, NUM_READINGS)) * 4 + np.random.normal(0, 0.5, NUM_READINGS)
    humids = base_humidity - np.sin(np.linspace(0, 4*np.pi, NUM_READINGS)) * 5 + np.random.normal(0, 2, NUM_READINGS)
    pressures = base_pressure + np.random.normal(0, 1.5, NUM_READINGS)
    
    rainfall_noise = np.random.rand(NUM_READINGS)
    rainfall = np.where(rainfall_noise > 0.95, np.random.uniform(0.1, 5.0, NUM_READINGS), 0)


    device_data = pd.DataFrame({
        'timestamp': timestamps,
        'temperature_c': temps.round(1),
        'humidity_perc': humids.clip(0, 100).round(1),
        'pressure_hpa': pressures.round(1),
        'rainfall_mm': rainfall.round(1),
        'status': 'Active'
    })
    data.append(device_data)

    df = pd.concat(data).sort_values('timestamp').reset_index(drop=True)
    
    # Log the full dataset to CSV (Simulated logging)
    # df.to_csv(DATA_LOG_PATH, index=False)
    
    return df

# --- DATA PARSING AND LOGGING (Placeholder functions) ---

def parse_serial_data(serial_line):
    """Placeholder for parsing the serial string into a dictionary."""
    # Example expected line: "T=25.5,H=65.2,P=1012.3,R=0.0"
    return {}

def log_forecast_data(forecast_df, ai_summary):
    """Placeholder for logging the AI forecast result."""
    pass