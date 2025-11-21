from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.combined import router as combined_router
from api.weather_api import router as weather_router
from api.latest_sensor import router as sensor_router
from api.ml_forecast import router as ml_router

app = FastAPI(title="WeatherStack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only these — Gemini removed
app.include_router(sensor_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(ml_router, prefix="/api")
app.include_router(combined_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "running"}
