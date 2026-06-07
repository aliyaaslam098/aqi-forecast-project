import os
os.environ["TMPDIR"] = "C:/tmp"

import requests
import pandas as pd
from datetime import datetime
import hopsworks

# ==========================================
# OPENWEATHER API SETTINGS
# ==========================================

API_KEY = "ba57b5a591714a8404a1f71b11f5acd1"

CITY = "Karachi"

LAT = 24.8607
LON = 67.0011

# ==========================================
# WEATHER API URL
# ==========================================

weather_url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?lat={LAT}"
    f"&lon={LON}"
    f"&appid={API_KEY}"
    f"&units=metric"
)

# ==========================================
# AQI API URL
# ==========================================

aqi_url = (
    f"https://api.openweathermap.org/data/2.5/air_pollution"
    f"?lat={LAT}"
    f"&lon={LON}"
    f"&appid={API_KEY}"
)

# ==========================================
# FETCH WEATHER DATA
# ==========================================

weather_response = requests.get(weather_url)
weather_data = weather_response.json()

print("\n==============================")
print("RAW WEATHER API RESPONSE")
print("==============================")
print(weather_data)

# ==========================================
# FETCH AQI DATA
# ==========================================

aqi_response = requests.get(aqi_url)
aqi_data = aqi_response.json()

print("\n==============================")
print("RAW AQI API RESPONSE")
print("==============================")
print(aqi_data)

# ==========================================
# EXTRACT WEATHER FEATURES
# ==========================================

temperature = weather_data["main"]["temp"]
humidity = weather_data["main"]["humidity"]
wind_speed = weather_data["wind"]["speed"]

# ==========================================
# EXTRACT AQI FEATURES
# ==========================================

aqi_category = aqi_data["list"][0]["main"]["aqi"]

components = aqi_data["list"][0]["components"]

co = components["co"]
no2 = components["no2"]
o3 = components["o3"]
so2 = components["so2"]
pm25 = components["pm2_5"]
pm10 = components["pm10"]

# ==========================================
# DATETIME FEATURES
# ==========================================

now = datetime.now()

hour = now.hour
day = now.day
month = now.month

# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame([{
    "datetime": str(now),
    "city": CITY,
    "temperature": temperature,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "pm25": pm25,
    "pm10": pm10,
    "co": co,
    "no2": no2,
    "o3": o3,
    "so2": so2,
    "aqi": aqi_category,
    "hour": hour,
    "day": day,
    "month": month
}])

print("\n==============================")
print("FEATURE DATA")
print("==============================")
print(df)

# ==========================================
# SAVE LOCAL CSV
# ==========================================

csv_file = "historical_aqi_dataset.csv"

try:

    old_df = pd.read_csv(csv_file)

    updated_df = pd.concat(
        [old_df, df],
        ignore_index=True
    )

except FileNotFoundError:

    updated_df = df

updated_df.to_csv(
    csv_file,
    index=False
)

print("\n==============================")
print("LOCAL CSV SAVED")
print("==============================")

# ==========================================
# CONNECT TO HOPSWORKS
# ==========================================

project = hopsworks.login(
    project="A_Q_I_P",
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

print("\n==============================")
print("CONNECTED TO HOPSWORKS")
print("==============================")

# ==========================================
# FEATURE STORE
# ==========================================

fs = project.get_feature_store()

# ==========================================
# FEATURE GROUP
# ==========================================

feature_group = fs.get_or_create_feature_group(

    name="aqi_features",

    version=2,

    description="AQI Forecasting Features",

    primary_key=["datetime"],

    online_enabled=True
)

print("\n==============================")
print("FEATURE GROUP READY")
print("==============================")

# ==========================================
# INSERT INTO FEATURE STORE
# ==========================================

feature_group.insert(df)

print("\n==============================")
print("DATA INSERTED TO HOPSWORKS")
print("==============================")

print("SUCCESS")