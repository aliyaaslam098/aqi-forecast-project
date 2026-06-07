import joblib

print("\n========================")
print("LOADING MODEL")
print("========================")

model = joblib.load(
    "aqi_forecast_model.pkl"
)

features = joblib.load(
    "model_features.pkl"
)

print("Model Loaded")
print("Features Loaded")

print("\nFeatures:")
print(features)