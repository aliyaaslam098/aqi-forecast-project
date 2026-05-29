from fastapi import FastAPI
import requests
import pandas as pd
import joblib
from datetime import datetime

app = FastAPI()

# =========================
# API SETTINGS
# =========================

API_KEY = "ba57b5a591714a8404a1f71b11f5acd1"
CITY = "Karachi"

# =========================
# LOAD TRAINED MODEL
# =========================

model = joblib.load("aqi_forecast_model.pkl")

# =========================
# FORECAST ENDPOINT
# =========================

@app.get("/forecast")
def forecast():

    # =========================
    # GET 5-DAY WEATHER FORECAST
    # =========================

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY}&appid={API_KEY}&units=metric"
    )

    response = requests.get(forecast_url)
    data = response.json()

    forecast_list = data["list"]

    results = []

    # Take one prediction per day
    selected_forecasts = [
        forecast_list[0],
        forecast_list[8],
        forecast_list[16]
    ]

    # Dummy lag AQI values
    previous_aqi_1 = 60
    previous_aqi_2 = 55

    for item in selected_forecasts:

        temperature = item["main"]["temp"]
        humidity = item["main"]["humidity"]
        wind_speed = item["wind"]["speed"]

        dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")

        hour = dt.hour
        day = dt.day
        month = dt.month

        # Create dataframe
        features = pd.DataFrame([{
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "hour": hour,
            "day": day,
            "month": month,
            "aqi_lag_1": previous_aqi_1,
            "aqi_lag_2": previous_aqi_2
        }])

        # Predict AQI
        predicted_aqi = model.predict(features)[0]

        results.append({
            "date": dt.strftime("%Y-%m-%d"),
            "temperature": round(temperature, 2),
            "humidity": humidity,
            "wind_speed": wind_speed,
            "predicted_aqi": round(predicted_aqi, 2)
        })

        # Update lag values
        previous_aqi_2 = previous_aqi_1
        previous_aqi_1 = predicted_aqi

    return {
        "city": CITY,
        "forecast": results
    }