import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("\n===================================")
print("DATA LEAKAGE VALIDATION")
print("===================================")

# ===========================
# LOAD DATA
# ===========================

df = pd.read_csv("historical_aqi_dataset.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month

df["aqi_lag_1"] = df["aqi"].shift(1)
df["aqi_lag_2"] = df["aqi"].shift(2)

df = df.dropna()

# ==================================================
# MODEL A
# WEATHER ONLY
# ==================================================

weather_features = [
    "temperature",
    "humidity",
    "wind_speed",
    "pressure",
    "cloud_cover",
    "precipitation",
    "hour",
    "day",
    "month"
]

X = df[weather_features]
y = df["aqi"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\nMODEL A (WEATHER ONLY)")
print("--------------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 2))

# ==================================================
# MODEL B
# WEATHER + AQI LAGS
# ==================================================

all_features = [
    "temperature",
    "humidity",
    "wind_speed",
    "pressure",
    "cloud_cover",
    "precipitation",
    "hour",
    "day",
    "month",
    "aqi_lag_1",
    "aqi_lag_2"
]

X = df[all_features]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

model = LinearRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\nMODEL B (WITH AQI LAGS)")
print("--------------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 2))