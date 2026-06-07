import pandas as pd
import numpy as np
import joblib
import hopsworks

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =====================================
# CONNECT TO HOPSWORKS
# =====================================
print("\n🔗 Connecting to Hopsworks...")

project = hopsworks.login(
    project="A_Q_I_P",
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

fs = project.get_feature_store()

print("✅ Connected Successfully")

# =====================================
# LOAD FEATURE GROUP
# =====================================
print("\n📥 Loading Feature Group...")

fg = fs.get_feature_group(
    name="aqi_features",
    version=1
)

df = fg.read()

print("✅ Data Loaded")
print("Shape:", df.shape)

# =====================================
# CHECK EMPTY DATA
# =====================================
if df.empty:

    print("\n❌ Feature Group is empty!")
    print("Run features.py first.")

    exit()

# =====================================
# DISPLAY DATA INFO
# =====================================
print("\n📋 Columns:")
print(df.columns.tolist())

print("\n📈 Dataset Statistics:")
print(df.describe())

# =====================================
# CLEAN DATA
# =====================================
df = df.dropna()

# =====================================
# REQUIRED COLUMNS CHECK
# =====================================
required_columns = [
    "temperature",
    "humidity",
    "wind_speed",
    "aqi"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print("\n❌ Missing Required Columns:")
    print(missing_columns)

    exit()

# =====================================
# DATETIME FEATURES
# =====================================
if "datetime" in df.columns:

    print("\n🕒 Creating datetime features...")

    df["datetime"] = pd.to_datetime(df["datetime"])

    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day
    df["month"] = df["datetime"].dt.month

else:

    print("\n⚠️ datetime column missing")
    print("Using default values")

    df["hour"] = 12
    df["day"] = 1
    df["month"] = 1

# =====================================
# LAG FEATURES
# =====================================
print("\n📊 Creating lag features...")

df["aqi_lag_1"] = df["aqi"].shift(1)
df["aqi_lag_2"] = df["aqi"].shift(2)

# remove NaNs from lagging
df = df.dropna()

# =====================================
# FEATURES & TARGET
# =====================================
features = [
    "temperature",
    "humidity",
    "wind_speed",
    "hour",
    "day",
    "month",
    "aqi_lag_1",
    "aqi_lag_2"
]

X = df[features]

y = df["aqi"]

print("\n✅ Features Ready")
print("Feature Shape:", X.shape)

# =====================================
# TRAIN TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# =====================================
# MODELS
# =====================================
models = {

    "RandomForest": RandomForestRegressor(
        n_estimators=20,
        random_state=42
    ),

    "LinearRegression": LinearRegression()
}

best_model = None
best_rmse = float("inf")

# =====================================
# TRAINING LOOP
# =====================================
for name, model in models.items():

    print(f"\n🚀 Training {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    print(f"\n{name} Results")
    print("MAE  :", round(mae, 3))
    print("RMSE :", round(rmse, 3))
    print("R²   :", round(r2, 3))

    if rmse < best_rmse:

        best_rmse = rmse
        best_model = model
        best_model_name = name

# =====================================
# SAVE MODEL
# =====================================
joblib.dump(
    best_model,
    "aqi_forecast_model.pkl"
)

print(f"\n🏆 Best Model: {best_model_name}")

print("✅ Model Saved Successfully")