# ==============================
# IMPORT LIBRARIES
# ==============================
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


# ==============================
# STEP 1: LOAD ENV VARIABLES
# ==============================
load_dotenv()

API_KEY = os.getenv("ba57b5a591714a8404a1f71b11f5acd1")
CITY = os.getenv("CITY")

if not API_KEY or not CITY:
    raise ValueError("❌ API_KEY or CITY not found in .env file")


# ==============================
# STEP 2: WEATHER API CALL
# ==============================
weather_url = "https://api.openweathermap.org/data/2.5/weather?q=Karachi&appid=32e3fab605a89fe784cfb9c35b5e5872&units=metric"
weather_response = requests.get(weather_url).json()

if 'main' not in weather_response:
    print("❌ Weather API Error:", weather_response)
    exit()

temperature = weather_response['main']['temp']
humidity = weather_response['main']['humidity']
wind_speed = weather_response['wind']['speed']


# ==============================
# STEP 3: GET COORDINATES
# ==============================
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY}&limit=1&appid={API_KEY}"
geo_response = requests.get(geo_url).json()

if not geo_response:
    print("❌ Geo API Error")
    exit()

lat = geo_response[0]['lat']
lon = geo_response[0]['lon']


# ==============================
# STEP 4: AQI API CALL
# ==============================
aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
aqi_response = requests.get(aqi_url).json()

if 'list' not in aqi_response:
    print("❌ AQI API Error:", aqi_response)
    exit()

aqi_value = aqi_response['list'][0]['main']['aqi']


# ==============================
# STEP 5: CREATE RECORD
# ==============================
record = {
    "datetime": datetime.now(),
    "city": CITY,
    "latitude": lat,
    "longitude": lon,
    "temperature": temperature,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "aqi": aqi_value
}


# ==============================
# STEP 6: SAVE TO CSV (FIXED)
# ==============================
df = pd.DataFrame([record])

file_path = "aqi_data.csv"

file_exists = os.path.exists(file_path)

df.to_csv(
    file_path,
    mode='a',                 # append mode
    header=not file_exists,   # write header only first time
    index=False
)

print("✅ Data saved successfully")