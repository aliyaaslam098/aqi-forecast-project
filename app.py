from fastapi import FastAPI
import requests
import pandas as pd
import joblib
from datetime import datetime

app = FastAPI()

# =========================
# SETTINGS
# =========================

CITY = "Karachi"

# =========================
# LOAD MODEL
# =========================

model = joblib.load("aqi_forecast_model.pkl")

# =========================
# FORECAST ENDPOINT
# =========================

@app.get("/forecast")
def forecast():

    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=24.8607"
        "&longitude=67.0011"
        "&daily="
        "temperature_2m_max,"
        "relative_humidity_2m_mean,"
        "precipitation_sum,"
        "wind_speed_10m_max,"
        "pressure_msl_mean,"
        "cloud_cover_mean"
        "&forecast_days=3"
        "&timezone=auto"
    )

    response = requests.get(forecast_url)

    data = response.json()

    daily = data["daily"]

    # Load latest AQI history
    history = pd.read_csv(
        "historical_aqi_dataset.csv"
    )

    previous_aqi_1 = history["aqi"].iloc[-1]
    previous_aqi_2 = history["aqi"].iloc[-2]
    results = []

    for i in range(3):

        date_str = daily["time"][i]

        temperature = daily["temperature_2m_max"][i]

        humidity = daily["relative_humidity_2m_mean"][i]

        wind_speed = daily["wind_speed_10m_max"][i]

        pressure = daily["pressure_msl_mean"][i]

        cloud_cover = daily["cloud_cover_mean"][i]

        precipitation = daily["precipitation_sum"][i]

        dt = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        )

        features = pd.DataFrame([{
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "cloud_cover": cloud_cover,
            "precipitation": precipitation,
            "hour": 12,
            "day": dt.day,
            "month": dt.month,
            "aqi_lag_1": previous_aqi_1,
            "aqi_lag_2": previous_aqi_2
        }])

        predicted_aqi = model.predict(features)[0]

        if predicted_aqi <= 50:
            category = "Good"

        elif predicted_aqi <= 100:
            category = "Moderate"

        elif predicted_aqi <= 150:
            category = "Unhealthy for Sensitive Groups"

        elif predicted_aqi <= 200:
            category = "Unhealthy"

        elif predicted_aqi <= 300:
            category = "Very Unhealthy"

        else:
            category = "Hazardous"

        results.append({
            "date": date_str,
            "temperature": round(float(temperature), 2),
            "humidity": round(float(humidity), 2),
            "wind_speed": round(float(wind_speed), 2),
            "pressure": round(float(pressure), 2),
            "cloud_cover": round(float(cloud_cover), 2),
            "precipitation": round(float(precipitation), 2),
            "predicted_aqi": round(float(predicted_aqi), 2),
            "category": category
        })

        # Update lag values for next day
        previous_aqi_2 = previous_aqi_1
        previous_aqi_1 = predicted_aqi

    return {
        "city": CITY,
        "forecast": results
    }