
import os
import pandas as pd
import hopsworks

# ===============================
# WINDOWS TEMP FIX
# ===============================
os.environ["TMP"] = "C:\\Temp"
os.environ["TEMP"] = "C:\\Temp"

# ===============================
# LOGIN TO HOPSWORKS
# ===============================
project = hopsworks.login(
    project="A_Q_I_P",
    host="eu-west.cloud.hopsworks.ai",
    port=443,
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

print("✅ Connected to Hopsworks")

# ===============================
# GET FEATURE STORE
# ===============================
fs = project.get_feature_store()

print("✅ Feature Store Connected")

# ===============================
# LOAD CSV
# ===============================
df = pd.read_csv("aqi_data.csv")

print(df.head())

# ===============================
# CLEAN DATA
# ===============================
df = df.dropna()

# create id if not exists
if "id" not in df.columns:
    df["id"] = range(len(df))

# ===============================
# CREATE FEATURE GROUP
# ===============================
fg = fs.get_or_create_feature_group(
    name="aqi_features",
    version=1,
    primary_key=["id"],
    description="AQI Prediction Dataset"
)

print("✅ Feature Group Ready")

# ===============================
# INSERT INTO FEATURE STORE
# ===============================
fg.insert(df)

print("🚀 Upload Complete")