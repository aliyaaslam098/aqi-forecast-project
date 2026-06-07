import requests
import pandas as pd

LATITUDE = 24.8607
LONGITUDE = 67.0011

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=24.8607"
    "&longitude=67.0011"
    "&start_date=2026-03-01"
    "&end_date=2026-05-31"
    "&hourly=temperature_2m,"
"relative_humidity_2m,"
"wind_speed_10m,"
"surface_pressure,"
"cloud_cover,"
"precipitation"
)

response = requests.get(url)

data = response.json()

df = pd.DataFrame({
    "datetime": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "wind_speed": data["hourly"]["wind_speed_10m"],
    "pressure": data["hourly"]["surface_pressure"],
    "cloud_cover": data["hourly"]["cloud_cover"],
    "precipitation": data["hourly"]["precipitation"]
})

print(df.head())

df.to_csv(
    "karachi_historical_weather.csv",
    index=False
)

print("\nSaved:")
print("karachi_historical_weather.csv")