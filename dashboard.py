import streamlit as st
import requests
import pandas as pd

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AQI Forecast Dashboard",
    page_icon="🌍",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🌍 AQI Forecast Dashboard")
st.subheader("Live Air Quality Prediction System")

# =========================
# CALL FASTAPI
# =========================

API_URL = "http://127.0.0.1:8000/forecast"

response = requests.get(API_URL)

data = response.json()

forecast_data = data["forecast"]

# =========================
# CURRENT DAY
# =========================

today = forecast_data[0]

# =========================
# TOP METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("City", data["city"])
col2.metric("Temperature", f"{today['temperature']} °C")
col3.metric("Humidity", f"{today['humidity']}%")
col4.metric("Wind Speed", f"{today['wind_speed']} m/s")

# =========================
# AQI DISPLAY
# =========================

aqi_value = today["predicted_aqi"]

st.divider()

st.markdown(f"# Predicted AQI: {aqi_value}")

# AQI Status
if aqi_value <= 50:
    st.success("AQI Status: Good 😊")

elif aqi_value <= 100:
    st.warning("AQI Status: Moderate 😐")

else:
    st.error("AQI Status: Unhealthy 😷")

# =========================
# FORECAST TABLE
# =========================

st.divider()

st.subheader("3-Day AQI Forecast")

forecast_df = pd.DataFrame(forecast_data)

st.dataframe(forecast_df)

# =========================
# CHART
# =========================

st.subheader("AQI Forecast Trend")

chart_df = forecast_df[["date", "predicted_aqi"]]

chart_df = chart_df.set_index("date")

st.line_chart(chart_df)

# =========================
# FOOTER
# =========================

st.divider()

st.caption("Live AQI Forecasting System using FastAPI + Streamlit + ML")