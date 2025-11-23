[![Image Unavailable](aeroLogo.png)]()

# AeroSync - Weather Prediction System 🌤️

A comprehensive IoT-based weather prediction system that collects real-time sensor data, integrates with WeatherAPI, trains machine learning models, and provides forecasts through a modern web interface powered by FastAPI backend and NiceGUI dashboard with beautiful visualizations.

## 🌟 Features

### Data Collection & Integration
- **Real-time IoT Sensor Data**: Serial reader for ESP32/Arduino weather station sensors
- **WeatherAPI Integration**: Fetches current weather and 7-day forecasts
- **Automatic Fallback**: Falls back to WeatherAPI when IoT sensor is disconnected (30-min freshness check)
- **Database Storage**: SQLite database for historical data and forecasts

### Machine Learning
- **Random Forest Model**: Temperature prediction based on historical data
- **7-Day ML Forecast**: AI-powered predictions for temperature trends
- **Automated Training**: Train models on collected sensor data

### Interactive Dashboard
- **NiceGUI Interface**: Modern, responsive web UI with glassmorphism design (runs on port 8080)
- **FastAPI Backend**: RESTful API server (runs on port 8000)
- **Dark/Light Theme**: Toggle between themes with persistent preferences
- **Real-time Updates**: Live sensor status indicator (Connected/Disconnected)
- **Beautiful Charts**: Interactive Plotly visualizations for trends
- **7-Day Forecast**: Combined WeatherAPI + ML predictions

### Visualizations
- **Temperature Trend**: AI predictions vs API bounds (filled area chart)
- **Humidity Trend**: Historical humidity data (7 days)
- **Pressure Trend**: Atmospheric pressure trends
- **Rainfall Chart**: Daily rainfall bar chart
- **All charts support light/dark themes**

### API Features
- **FastAPI Backend**: RESTful API for all data operations
- **Combined Endpoint**: Merges IoT, WeatherAPI, and ML data
- **Manual Sync**: "Sync WeatherAPI" button to fetch and store forecasts
- **ML Trigger**: "Trigger ML Forecast" button for on-demand predictions

## 📋 Project Structure

```
app2/
├── main.py                     # FastAPI + NiceGUI application entry point
├── api/
│   ├── combined.py             # Combined weather data endpoint
│   ├── latest_sensor.py        # Latest IoT sensor reading
│   ├── weather_api.py          # WeatherAPI integration
│   ├── ml_forecast.py          # ML prediction endpoint
│   ├── gemini_forecast.py      # Gemini AI integration
│   └── train_ml_model.py       # ML model training pipeline
├── ui/
│   └── ui.py                   # NiceGUI dashboard interface
├── db/
│   └── db.py                   # Database operations (SQLite)
├── serial/
│   └── serial_reader.py        # IoT sensor data collection
├── utils/
│   └── theme_manager.py        # Dark/light theme management
├── services/
│   ├── condition_map.py        # Weather condition mapping
│   ├── merger.py               # Data merging utilities
│   └── utils.py                # Helper functions
├── core/
│   └── config.py               # Configuration management
├── hardware/
│   └── weather_station.ino     # Arduino/ESP32 firmware
├── assets/
│   └── themes/                 # UI theme definitions
├── requirements.txt            # Python dependencies
├── run.sh                      # Linux/Mac startup script
├── run.bat                     # Windows startup script
└── README.md                   # This file
```

## 🛠️ Tech Stack

### Backend
- **Python 3.12+**
- **FastAPI**: Modern web framework for APIs
- **NiceGUI**: Python-based web UI framework
- **SQLite**: Lightweight database

### Data Science
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **Joblib**: Model persistence

### Visualization
- **Plotly**: Interactive charts

### Hardware
- **Arduino**: IoT weather station
- **DHT-22**: Temperature and humidity sensor
- **BMP280**: Pressure sensor
- **Rain Gauge**: GPIO-based rainfall detection

### External APIs
- **WeatherAPI**: Current weather and forecasts

## 📦 Dependencies

```
pandas
numpy
scikit-learn
joblib
pyserial
plotly
adafruit-circuitpython-bmp280
python-dotenv
fastapi
uvicorn[standard]
nicegui
requests
```

See `requirements.txt` for complete list.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

The script will:
1. Create virtual environment (if needed)
2. Install dependencies
3. Start serial reader (background)
4. Start FastAPI + NiceGUI server
5. Open dashboard in browser at `http://localhost:8000`

### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd app2
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy the example file and edit with your values:
   ```bash
   cp .env.example .env
   # Then edit .env with your actual API keys and configuration
   ```
   
   Required variables:
   - `WEATHERAPI_KEY` - Get from https://www.weatherapi.com/
   - `CITY_NAME` - Your location (e.g., "New Town, West Bengal")
   - `API_BASE` - Backend URL (default: http://localhost:8000)

5. **Run components:**
   ```bash
   # Start serial reader (optional, for IoT sensor)
   python serial/serial_reader.py &
   
   # Start FastAPI backend
   uvicorn main:app --host 0.0.0.0 --port 8000 &
   
   # Start NiceGUI dashboard
   python ui/ui.py
   ```

6. **Access the application:**
   - FastAPI Backend: `http://localhost:8000`
   - NiceGUI Dashboard: `http://localhost:8080`

## 📡 Hardware Setup

### Arduino Weather Station

1. **Upload firmware:**
   - Open `hardware/weather_station.ino` in Arduino IDE
   - Select your board (Arduino)
   - Upload to device

2. **Connect sensors:**
   - **DHT-22**: I2C connection (+, OUT, -)
   - **BMP280**: I2C connection (SDA, SCL)
   - **Rain Gauge**: GPIO pin (configurable)
   - **OLED-DISPLAY**: If Available

4. **Configure serial port:**
   Update `.env` or `serial/serial_reader.py`:
   ```python
   SERIAL_PORT = "/dev/ttyUSB0"  # Linux/Mac
   # or
   SERIAL_PORT = "COM3"  # Windows
   ```

### Supported Sensors
- **Temperature**: DHT-22 (°C)
- **Humidity**: DHT-22 (%)
- **Pressure**: BMP280 (hPa)
- **Rainfall**: GPIO-based rain gauge (mm)

## 🤖 Machine Learning

### Model Details
- **Algorithm**: Random Forest Regressor
- **Features**:
  - Historical temperature
  - Humidity percentage
  - Atmospheric pressure
  - Rainfall
  - Time features (hour, day of year)
  - Rolling averages

### Training
```bash
python api/train_ml_model.py
```

Model is saved to `ml_weather_model.pkl` for predictions.

### Prediction
- Automatic: Via `/api/ml_forecast` endpoint
- Manual: Click "Trigger ML Forecast" button in dashboard

## 📊 Data Flow

1. **IoT Sensor** → Serial Reader → SQLite Database
2. **WeatherAPI** → Sync Endpoint → SQLite Database
3. **ML Model** → Training Script → `ml_weather_model.pkl`
4. **Combined API** → Merges IoT + WeatherAPI + ML → Dashboard
5. **Dashboard** → Displays charts, forecasts, current conditions

## 🎨 Dashboard Features

### Main Sections

1. **Hero Card** (Top-left)
   - Current temperature (large display)
   - Weather condition with emoji
   - Rainfall, Humidity, Wind (bottom row)

2. **Detail Cards** (Top-right, 2x2 grid)
   - Feels Like temperature
   - Atmospheric Pressure
   - Sunrise time
   - Sunset time

3. **7-Day Forecast** (Middle)
   - Day name, date, emoji, high/low temps
   - Merged WeatherAPI + ML predictions
   - Action buttons: "Trigger ML Forecast", "Sync WeatherAPI"

4. **Trend Charts** (Bottom, 2x2 grid)
   - **Temperature**: AI prediction vs API bounds
   - **Humidity**: 7-day trend
   - **Pressure**: 7-day trend
   - **Rainfall**: Daily totals (bar chart)

### Theme Toggle
- Click moon icon in header to switch between dark/light modes
- Preference persists across sessions

### IoT Status
- **Connected** (green): Sensor data is fresh (<30 min old)
- **Disconnected** (red): Sensor data is stale, using WeatherAPI fallback

## 🔐 Security Best Practices

- **API Keys**: Store in `.env` file (not committed to git)
- **Environment Variables**: Use `python-dotenv` for configuration
- **Virtual Environment**: Isolates dependencies
- **No hardcoded secrets**: All sensitive data in `.env`

## 🌐 Environment Variables

**For new users:** Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Then edit `.env` with your actual configuration:

```env
# WeatherAPI Configuration (REQUIRED)
WEATHERAPI_KEY=your_weatherapi_key_here
CITY_NAME=New Town, West Bengal

# API Configuration
API_BASE=http://localhost:8000

# Serial Port (optional, for IoT sensor)
SERIAL_PORT=/dev/ttyUSB0  # Linux/Mac
# SERIAL_PORT=COM3  # Windows
SERIAL_BAUD=9600

# Gemini API (optional, for AI forecasting)
# GEMINI_API_KEY=your_gemini_key_here
```

See `.env.example` for detailed documentation of all available variables.

## 🐛 Troubleshooting

### Virtual environment not activating
```bash
python3 -m venv venv --clear
source venv/bin/activate
```

### Serial port not found
- **Linux/Mac**: Check with `ls /dev/tty*`
- **Windows**: Check Device Manager
- Update `SERIAL_PORT` in `.env`

### Dashboard not loading
```bash
# Check if port 8000 is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Try different port
uvicorn main:app --port 8001
```

### Charts not displaying data
- Ensure database has data: `ls -lh weather_data.db`
- Check if serial reader is running
- Verify WeatherAPI key is valid

### Model training fails
- Ensure database has sufficient data (at least 7 days)
- Check for missing columns in readings table

## 📈 API Endpoints

### Weather Data
- `GET /api/combined` - Combined IoT + WeatherAPI + ML data
- `GET /api/latest_sensor` - Latest IoT sensor reading
- `GET /api/weatherapi/now` - Current weather from API
- `GET /api/weatherapi/7day` - 7-day forecast from API

### ML & Forecasting
- `GET /api/ml_forecast` - ML temperature predictions (7 days)
- `GET /api/gemini_forecast` - Gemini AI forecast

### Actions
- `GET /api/weatherapi/sync` - Fetch and store WeatherAPI forecast

## 🔄 Continuous Operation

The system is designed to run 24/7:
- **Serial reader**: Collects sensor data continuously (background process)
- **FastAPI Backend**: RESTful API server at `http://localhost:8000`
- **NiceGUI Dashboard**: Web interface at `http://localhost:8080`
- **Database**: Stores all readings with timestamps
- **Auto-refresh**: Dashboard updates every 30 seconds
- **Fallback**: Automatic switch to WeatherAPI if sensor fails

## 📝 Future Enhancements

- [ ] Historical data page with date range selector
- [ ] Weather alerts and notifications
- [ ] Mobile-responsive design improvements
- [ ] Export data to CSV
- [ ] Multi-location support
- [ ] WebSocket real-time updates
- [ ] User authentication
- [ ] Cloud deployment (Docker, Kubernetes)

## 👤 Author

**FlareSome**

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check troubleshooting section above
- Review logs in `logs/` directory

### Connect with FlareSome

[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://linkedin.com/in/ashif-anowar-flareSome)
[![X](https://img.shields.io/badge/X-%23000000.svg?logo=X&logoColor=white)](https://x.com/flareSome07?t=O0SrexzD9_wauo-vk6Xlng&s=09)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail)](mailto:ashif.anowar0607@gmail.com)

---

**Last Updated**: November 2025
**Version**: 2.0.0
