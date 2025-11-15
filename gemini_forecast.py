import json
from datetime import datetime, timedelta

# NOTE: In a real-world application, you would replace this simulation
# with actual 'requests' or 'http' client code to interact with the Gemini API.

# 1. API Configuration Setup (for real-world reference)
API_KEY = ""
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"

# 2. Structured Data Schema for 7-Day Forecast
FORECAST_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "day": {"type": "STRING"},
            "temp_high_c": {"type": "NUMBER"},
            "temp_low_c": {"type": "NUMBER"},
            "rain_prob_perc": {"type": "INTEGER"},
            "condition": {"type": "STRING"},
        }
    }
}

# 3. System Instruction for AI Insights
SYSTEM_PROMPT = (
    "Act as an intelligent weather prediction system. Based on the provided current sensor data "
    " and the 7-day forecast, provide a concise, single-paragraph summary of the key weather "
    "trends, anomalies, and necessary user warnings for the upcoming week. "
    "Your tone should be professional and informative."
)

def get_gemini_forecast(current_data):
    """
    Simulates calling the Gemini API to get a structured 7-day forecast and a natural language summary.
    
    Args:
        current_data (pd.Series): The latest row of sensor data.
        
    Returns:
        tuple: (list of dicts for forecast, str for summary)
    """
    
    # 4. User Query (Grounding)
    latest_reading = current_data
    user_query = (
        f"Generate a 7-day weather forecast based on current conditions. "
        f"Current sensor data: Temperature={latest_reading['temperature_c']}°C, "
        f"Humidity={latest_reading['humidity_perc']}%, "
        f"Pressure={latest_reading['pressure_hpa']}hPa, "
        f"Rainfall={latest_reading['rainfall_mm']}mm. "
        f"Provide the structured forecast data and the natural language summary."
    )
    
    # --- SIMULATED API RESPONSE ---
    
    # Simulated Structured Forecast Data
    simulated_forecast_data = [
        {"day": "Today", "temp_high_c": 27, "temp_low_c": 21, "rain_prob_perc": 5, "condition": "Sunny"},
        {"day": "Tomorrow", "temp_high_c": 28, "temp_low_c": 22, "rain_prob_perc": 10, "condition": "Partly Cloudy"},
        {"day": "Day 3", "temp_high_c": 26, "temp_low_c": 19, "rain_prob_perc": 65, "condition": "Heavy Showers"},
        {"day": "Day 4", "temp_high_c": 24, "temp_low_c": 18, "rain_prob_perc": 80, "condition": "Thunderstorms"},
        {"day": "Day 5", "temp_high_c": 25, "temp_low_c": 19, "rain_prob_perc": 40, "condition": "Cloudy"},
        {"day": "Day 6", "temp_high_c": 27, "temp_low_c": 20, "rain_prob_perc": 15, "condition": "Mostly Sunny"},
        {"day": "Day 7", "temp_high_c": 29, "temp_low_c": 23, "rain_prob_perc": 5, "condition": "Warm and Clear"}
    ]
    
    # Simulated AI Insights Summary
    simulated_summary = (
        "The forecast indicates a significant weather shift mid-week, transitioning from warm, sunny conditions "
        "to a period of heavy precipitation on Days 3 and 4, marked by high rain probability and possible "
        "thunderstorms. Pressure is expected to dip, accompanying this change. Users should prepare for cooler, "
        "wet conditions during this time. The weather stabilizes towards the weekend, returning to clear skies and above-average temperatures by Day 7."
    )
    
    return simulated_forecast_data, simulated_summary