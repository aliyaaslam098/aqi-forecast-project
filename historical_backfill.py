import pandas as pd
import numpy as np

print("\n==========================")
print("LOADING REAL KARACHI WEATHER")
print("==========================")

df = pd.read_csv("karachi_historical_weather.csv")

print("Rows Loaded:", len(df))

# =====================================
# GENERATE AQI FROM REAL WEATHER
# =====================================

aqi_values = []

previous_aqi_1 = 60
previous_aqi_2 = 55

for _, row in df.iterrows():

    temperature = row["temperature"]
    humidity = row["humidity"]
    wind_speed = row["wind_speed"]

    pressure = row["pressure"]
    cloud_cover = row["cloud_cover"]
    precipitation = row["precipitation"]

    aqi = (
            0.25 * temperature
            + 0.10 * humidity
            - 0.60 * wind_speed
            + 0.005 * pressure
            + 0.03 * cloud_cover
            - 0.80 * precipitation
            + 0.20 * previous_aqi_1
            + 0.10 * previous_aqi_2
            + 35
            + np.random.normal(0, 3)
    )

    aqi = max(20, min(aqi, 300))

    aqi_values.append(round(aqi, 2))

    previous_aqi_2 = previous_aqi_1
    previous_aqi_1 = aqi

# =====================================
# ADD AQI
# =====================================

df["aqi"] = aqi_values

# =====================================
# SAVE TRAINING DATA
# =====================================

df.to_csv(
    "historical_aqi_dataset.csv",
    index=False
)

print("\n==========================")
print("DATASET CREATED")
print("==========================")

print(df.head())

print("\nRows:", len(df))
print("\nSaved: historical_aqi_dataset.csv")