import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import hopsworks

project = hopsworks.login(
    project="A_Q_I_P",
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

fs = project.get_feature_store()

print("\n================================")
print("LOADING DATASET")
print("================================")

df = pd.read_csv("historical_aqi_dataset.csv")

print(df.head())
print(df.columns)
print(df.shape)

# ====================================
# DATETIME FEATURES
# ====================================

df["datetime"] = pd.to_datetime(df["datetime"])

df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month

# ====================================
# LAG FEATURES
# ====================================

df["aqi_lag_1"] = df["aqi"].shift(1)
df["aqi_lag_2"] = df["aqi"].shift(2)

df = df.dropna(
    subset=[
        "aqi_lag_1",
        "aqi_lag_2"
    ]
)

required_columns = [
    "temperature",
    "humidity",
    "wind_speed",
    "aqi"
]

df = df.dropna(subset=required_columns)

# ====================================
# FEATURES
# ====================================

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

print("\nRows after cleaning:")
print(len(df))

X = df[FEATURES]
y = df["aqi"]

print("\nFeatures Shape:")
print(X.shape)

# ====================================
# TRAIN TEST SPLIT
# ====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# ====================================
# MODELS
# ====================================

models = {
    "RandomForest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),

    "LinearRegression": LinearRegression()
}

best_model = None
best_rmse = 999999

for name, model in models.items():

    print(f"\nTraining {name}")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    print("MAE :", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2  :", round(r2, 2))

    if rmse < best_rmse:

        best_rmse = rmse
        best_model = model
        best_model_name = name

# ====================================
# SAVE MODEL
# ====================================

joblib.dump(
    best_model,
    "aqi_forecast_model.pkl"
)

joblib.dump(
    FEATURES,
    "model_features.pkl"
)

print("\n================================")
print("BEST MODEL")
print("================================")

print(best_model_name)

print("\nModel saved:")
print("aqi_forecast_model.pkl")

print("Feature list saved:")
print("model_features.pkl")