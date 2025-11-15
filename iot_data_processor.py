def get_sensor_data(hours: int = 1):
    """
    Simulate IoT sensor data for the past 'hours' hours.
    Returns a DataFrame with standardized columns.
    """
    import random
    from datetime import datetime, timedelta
    import pandas as pd

    now = datetime.now()
    timestamps = [now - timedelta(hours=i) for i in range(hours)][::-1]

    data = []
    for t in timestamps:
        data.append({
            "timestamp": t,  # 👈 store actual datetime object, not str
            "temperature_c": round(random.uniform(20.0, 35.0), 2),
            "humidity_perc": round(random.uniform(40.0, 85.0), 2),
            "pressure_hpa": round(random.uniform(980.0, 1025.0), 2),
            "rainfall_mm": round(random.uniform(0.0, 10.0), 2)
        })

    df = pd.DataFrame(data)
    return df
