import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -----------------------------
# SETTINGS
# -----------------------------
NUM_ROWS = 1000

# -----------------------------
# GENERATE HISTORICAL DATA
# -----------------------------
data = []

start_date = datetime.now() - timedelta(days=1000)

aqi_previous_1 = 50
aqi_previous_2 = 48

for i in range(NUM_ROWS):

    current_date = start_date + timedelta(hours=i)

    # Simulated weather values
    temperature = round(random.uniform(20, 42), 2)
    humidity = round(random.uniform(30, 90), 2)
    wind_speed = round(random.uniform(1, 12), 2)

    # Time features
    hour = current_date.hour
    day = current_date.day
    month = current_date.month

    # Simulated AQI formula
    aqi = (
        0.6 * temperature
        + 0.3 * humidity
        - 1.5 * wind_speed
        + 0.4 * aqi_previous_1
        + 0.2 * aqi_previous_2
        + random.uniform(-10, 10)
    )

    aqi = round(max(0, min(aqi, 300)), 2)

    # Save row
    data.append({
        "datetime": current_date,
        "city": "Karachi",
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "hour": hour,
        "day": day,
        "month": month,
        "aqi_lag_1": aqi_previous_1,
        "aqi_lag_2": aqi_previous_2,
        "aqi": aqi
    })

    # Update lag values
    aqi_previous_2 = aqi_previous_1
    aqi_previous_1 = aqi

# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame(data)

# -----------------------------
# SAVE CSV
# -----------------------------
df.to_csv("historical_aqi_dataset.csv", index=False)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
print("\n==============================")
print("HISTORICAL DATA GENERATED")
print("==============================")

print(df.head())

print("\n==============================")
print("SUCCESS")
print("==============================")

print(f"Rows generated: {len(df)}")
print("Saved as historical_aqi_dataset.csv")