import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("historical_aqi_dataset.csv")

# =========================
# FEATURES
# =========================

X = df[[
    "temperature",
    "humidity",
    "wind_speed",
    "hour",
    "day",
    "month",
    "aqi_lag_1",
    "aqi_lag_2"
]]

# =========================
# LOAD MODEL
# =========================

model = joblib.load("aqi_forecast_model.pkl")

# =========================
# CREATE SHAP EXPLAINER
# =========================

explainer = shap.TreeExplainer(model)

# =========================
# CALCULATE SHAP VALUES
# =========================

shap_values = explainer.shap_values(X)

# =========================
# SUMMARY PLOT
# =========================

print("\nGenerating SHAP summary plot...")

shap.summary_plot(
    shap_values,
    X,
    show=False
)

plt.savefig("shap_summary.png")

print("\nSUCCESS")
print("SHAP summary saved as shap_summary.png")