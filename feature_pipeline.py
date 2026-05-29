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

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# ==========================================
# AQI API URL
# ==========================================

aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# ==========================================
# FETCH WEATHER DATA
# ==========================================

weather_response = requests.get(weather_url)

weather_data = weather_response.json()

print("\n===================================")
print("RAW WEATHER API RESPONSE")
print("===================================")

print(weather_data)

# ==========================================
# FETCH AQI DATA
# ==========================================

aqi_response = requests.get(aqi_url)

aqi_data = aqi_response.json()

print("\n===================================")
print("RAW AQI API RESPONSE")
print("===================================")

print(aqi_data)

# ==========================================
# EXTRACT FEATURES
# ==========================================

temperature = weather_data["main"]["temp"]

humidity = weather_data["main"]["humidity"]

wind_speed = weather_data["wind"]["speed"]

aqi = aqi_data["list"][0]["main"]["aqi"]

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
    "aqi": aqi,
    "hour": hour,
    "day": day,
    "month": month
}])

print("\n===================================")
print("FEATURE DATA")
print("===================================")

print(df)

# ==========================================
# SAVE LOCAL CSV
# ==========================================

csv_file = "historical_aqi_dataset.csv"

try:

    old_df = pd.read_csv(csv_file)

    updated_df = pd.concat([old_df, df], ignore_index=True)

except FileNotFoundError:

    updated_df = df

updated_df.to_csv(csv_file, index=False)

print("\n===================================")
print("LOCAL CSV SAVED")
print("===================================")

print(f"Data saved to {csv_file}")

# ==========================================
# CONNECT TO HOPSWORKS
# ==========================================

project = hopsworks.login(
    project="A_Q_I_P",
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

print("\n===================================")
print("CONNECTED TO HOPSWORKS")
print("===================================")

# ==========================================
# GET FEATURE STORE
# ==========================================

fs = project.get_feature_store()

# ==========================================
# CREATE FEATURE GROUP
# ==========================================

feature_group = fs.get_or_create_feature_group(

    name="weather_features",

    version=1,

    description="Weather and AQI features for forecasting",

    primary_key=["datetime"],

    online_enabled=True
)

print("\n===================================")
print("FEATURE GROUP READY")
print("===================================")

# ==========================================
# INSERT DATA INTO FEATURE STORE
# ==========================================

feature_group.insert(df)

print("\n===================================")
print("DATA INSERTED INTO HOPSWORKS")
print("===================================")

print("SUCCESS")