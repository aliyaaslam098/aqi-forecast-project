import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv("historical_aqi_dataset.csv")

print("\n=====================================")
print("DATASET LOADED")
print("=====================================")

print(df.head())

# =====================================
# SELECT FEATURES
# =====================================

X = df[
    [
        "temperature",
        "humidity",
        "wind_speed",
        "hour",
        "day",
        "month",
        "aqi_lag_1",
        "aqi_lag_2"
    ]
]

# =====================================
# TARGET COLUMN
# =====================================

y = df["aqi"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\n=====================================")
print("TRAIN TEST SPLIT COMPLETE")
print("=====================================")

print(f"Training Rows: {len(X_train)}")
print(f"Testing Rows : {len(X_test)}")

# =====================================
# CREATE MODEL
# =====================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# =====================================
# TRAIN MODEL
# =====================================

print("\n=====================================")
print("TRAINING MODEL...")
print("=====================================")

model.fit(X_train, y_train)

# =====================================
# MAKE PREDICTIONS
# =====================================

predictions = model.predict(X_test)

# =====================================
# EVALUATE MODEL
# =====================================

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n=====================================")
print("MODEL EVALUATION")
print("=====================================")

print(f"MAE Score : {round(mae, 2)}")
print(f"MSE Score : {round(mse, 2)}")
print(f"R2 Score  : {round(r2, 2)}")

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(model, "aqi_forecast_model.pkl")

print("\n=====================================")
print("SUCCESS")
print("=====================================")

print("Model saved as:")
print("aqi_forecast_model.pkl")