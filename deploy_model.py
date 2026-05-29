import hopsworks
import time

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

# wait a bit for registration sync
time.sleep(10)

# ===============================
# GET MODEL
# ===============================
model = mr.get_model(
    name="aqi_prediction_model",
    version=5
)

print(model)

# ===============================
# DEPLOY
# ===============================
deployment = model.deploy(
    name="aqi_deployment"
)

deployment.start()

print("🚀 Deployment Started")