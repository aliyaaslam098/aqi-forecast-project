import requests
import pandas as pd
from datetime import datetime
import time
import random

# ==================================
# CONFIG
# ==================================
API_KEY = "dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"

LATITUDE = 24.8607
LONGITUDE = 67.0011

CITY = "Karachi,PK"

CSV_FILE = "aqi_data.csv"

# ==================================
# AQI CATEGORY → REALISTIC AQI
# ==================================
aqi_mapping = {
    1: random.randint(20, 50),
    2: random.randint(51, 100),
    3: random.randint(101, 150),
    4: random.randint(151, 200),
    5: random.randint(201, 300)
}

# ==================================
# FETCH WEATHER
# ==================================
weather_url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?lat={LATITUDE}"
    f"&lon={LONGITUDE}"
    f"&appid={API_KEY}"
    f"&units=metric"
)

# ==================================
# FETCH AQI
# ==================================
aqi_url = (
    f"https://api.openweathermap.org/data/2.5/air_pollution"
    f"?lat={LATITUDE}"
    f"&lon={LONGITUDE}"
    f"&appid={API_KEY}"
)

# ==================================
# GET WEATHER DATA
# ==================================
weather_response = requests.get(weather_url)
weather_data = weather_response.json()
print(weather_data)
# ==================================
# GET AQI DATA
# ==================================
aqi_response = requests.get(aqi_url)
aqi_data = aqi_response.json()
print(aqi_data)
# ==================================
# EXTRACT VALUES
# ==================================
temperature = weather_data["main"]["temp"]

humidity = weather_data["main"]["humidity"]

wind_speed = weather_data["wind"]["speed"]

aqi_category = aqi_data["list"][0]["main"]["aqi"]

realistic_aqi = aqi_mapping[aqi_category]

# ==================================
# CREATE ROW
# ==================================
row = {
    "datetime": datetime.now(),
    "city": CITY,
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "temperature": temperature,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "aqi": realistic_aqi
}

# ==================================
# SAVE TO CSV
# ==================================
df = pd.DataFrame([row])

try:

    existing_df = pd.read_csv(CSV_FILE)

    updated_df = pd.concat(
        [existing_df, df],
        ignore_index=True
    )

except:

    updated_df = df

updated_df.to_csv(
    CSV_FILE,
    index=False
)

print("✅ Data Collected Successfully")

print(updated_df.tail())