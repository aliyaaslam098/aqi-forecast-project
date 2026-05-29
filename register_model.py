import hopsworks

# ===============================
# LOGIN
# ===============================
project = hopsworks.login(
    project="A_Q_I_P",
    host="eu-west.cloud.hopsworks.ai",
    port=443,
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

print("✅ Connected to Hopsworks")

# ===============================
# MODEL REGISTRY
# ===============================
mr = project.get_model_registry()

# ===============================
# CREATE MODEL
# ===============================
model = mr.python.create_model(
    name="aqi_prediction_model",
    metrics={
        "accuracy": 0.95
    },
    description="AQI prediction model"
)

# ===============================
# SAVE MODEL ARTIFACTS
# ===============================
model.save("model_artifacts")

print("🚀 Model Registered Successfully")