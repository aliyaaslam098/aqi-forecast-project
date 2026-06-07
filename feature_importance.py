import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("historical_aqi_dataset.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month

df["aqi_lag_1"] = df["aqi"].shift(1)
df["aqi_lag_2"] = df["aqi"].shift(2)

df = df.dropna()

FEATURES = [
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

X = df[FEATURES]
y = df["aqi"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

importance = pd.Series(
    model.feature_importances_,
    index=FEATURES
)

importance.sort_values().plot.barh()

plt.title("Feature Importance")

plt.tight_layout()

plt.savefig("feature_importance.png")

plt.show()