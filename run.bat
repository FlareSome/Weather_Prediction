@echo off
REM Batch file to run Weather Prediction System on Windows

echo.
echo 🌤️  Weather Prediction System - Starting...
echo.

REM Check if venv exists, if not create it
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing/updating requirements...
pip install -r requirements.txt --quiet

echo.
echo 🚀 Starting Weather Prediction System...
echo.

REM Start serial reader in background (optional - comment out if no IoT sensor)
echo 1️⃣  Starting serial reader (IoT sensor)...
start /B python serial\serial_reader.py
timeout /t 2 /nobreak

REM Start main application (FastAPI + NiceGUI)
echo 2️⃣  Starting FastAPI + NiceGUI dashboard...
echo.
echo 📊 Dashboard will be available at: http://localhost:8000
echo.

python main.py

echo.
echo ✅ System stopped.
echo.

pause
