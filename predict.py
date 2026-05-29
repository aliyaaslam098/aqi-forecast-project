import joblib
import pandas as pd
from datetime import datetime, timedelta

# Load model
model = joblib.load("aqi_forecast_model.pkl")

# Get latest row
df = pd.read_csv("aqi_features.csv")
latest = df.iloc[-1]

predictions = []

current_time = datetime.now()

for i in range(72):  # 72 hours = 3 days
    future_time = current_time + timedelta(hours=i)

    input_data = pd.DataFrame([{
        "temperature": latest['temperature'],
        "humidity": latest['humidity'],
        "wind_speed": latest['wind_speed'],
        "hour": future_time.hour,
        "day": future_time.day,
        "month": future_time.month,
        "aqi_lag_1": latest['aqi'],
        "aqi_lag_2": latest['aqi_lag_1']
    }])

    pred = model.predict(input_data)[0]

    predictions.append((future_time, pred))

# Print results
for time, val in predictions[:10]:
    print(time, "→ AQI:", round(val, 2))