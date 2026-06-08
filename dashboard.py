import streamlit as st
import requests
import pandas as pd
import joblib
from datetime import datetime


st.set_page_config(
    page_title="SkyPulse",
    page_icon="🌍",
    layout="wide"
)
@st.cache_resource
def load_model():
    return joblib.load("aqi_forecast_model.pkl")

model = load_model()

CITY = "Karachi"

def fetch_forecast_data():
    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=24.8607"
        "&longitude=67.0011"
        "&daily="
        "temperature_2m_max,"
        "relative_humidity_2m_mean,"
        "precipitation_sum,"
        "wind_speed_10m_max,"
        "pressure_msl_mean,"
        "cloud_cover_mean"
        "&forecast_days=3"
        "&timezone=auto"
    )

    response = requests.get(forecast_url)

    data = response.json()

    daily = data["daily"]

    # Load latest AQI history
    history = pd.read_csv(
        "historical_aqi_dataset.csv"
    )

    previous_aqi_1 = history["aqi"].iloc[-1]
    previous_aqi_2 = history["aqi"].iloc[-2]
    results = []

    for i in range(3):

        date_str = daily["time"][i]

        temperature = daily["temperature_2m_max"][i]

        humidity = daily["relative_humidity_2m_mean"][i]

        wind_speed = daily["wind_speed_10m_max"][i]

        pressure = daily["pressure_msl_mean"][i]

        cloud_cover = daily["cloud_cover_mean"][i]

        precipitation = daily["precipitation_sum"][i]

        dt = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        )

        features = pd.DataFrame([{
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "cloud_cover": cloud_cover,
            "precipitation": precipitation,
            "hour": 12,
            "day": dt.day,
            "month": dt.month,
            "aqi_lag_1": previous_aqi_1,
            "aqi_lag_2": previous_aqi_2
        }])

        predicted_aqi = model.predict(features)[0]

        if predicted_aqi <= 50:
            category = "Good"

        elif predicted_aqi <= 100:
            category = "Moderate"

        elif predicted_aqi <= 150:
            category = "Unhealthy for Sensitive Groups"

        elif predicted_aqi <= 200:
            category = "Unhealthy"

        elif predicted_aqi <= 300:
            category = "Very Unhealthy"

        else:
            category = "Hazardous"

        results.append({
            "date": date_str,
            "temperature": round(float(temperature), 2),
            "humidity": round(float(humidity), 2),
            "wind_speed": round(float(wind_speed), 2),
            "pressure": round(float(pressure), 2),
            "cloud_cover": round(float(cloud_cover), 2),
            "precipitation": round(float(precipitation), 2),
            "predicted_aqi": round(float(predicted_aqi), 2),
            "category": category
        })

        # Update lag values for next day
        previous_aqi_2 = previous_aqi_1
        previous_aqi_1 = predicted_aqi

    return {
        "city": CITY,
        "forecast": results
    }

with st.sidebar:
    st.title("🌍 AQI Navigator")
    page = st.radio(
        "Select View",
        ["Dashboard", "Analytics", "Model", "System Info"]
    )

st.markdown("""
# 🌍 SKYPULSE

### Air Quality Intelligence & Forecasting Platform

📍 Karachi, Pakistan
""")

st.caption(
    "Developed by **Aliya Faisal** | Internship Project 2026 (May–June)"
)

st.info(
    "Powered by Open-Meteo, Machine Learning, FastAPI, Streamlit and Hopsworks"
)

data = fetch_forecast_data()

forecast_data = data["forecast"]
today = forecast_data[0]
forecast_df = pd.DataFrame(forecast_data)

if page == "Dashboard":

    st.divider()

    left, right = st.columns([1, 2])

    with left:
        st.subheader("Current AQI")
        st.metric(
            label="Karachi",
            value=f"{today['predicted_aqi']:.0f}"
        )

    with right:
        st.subheader("Atmospheric Conditions")

        row1_col1, row1_col2, row1_col3 = st.columns(3)

        row1_col1.metric(
            "🌡 Temperature",
            f"{today['temperature']} °C"
        )

        row1_col2.metric(
            "💧 Humidity",
            f"{today['humidity']} %"
        )

        row1_col3.metric(
            "🌬 Wind Speed",
            f"{today['wind_speed']} km/h"
        )

        row2_col1, row2_col2, row2_col3 = st.columns(3)

        row2_col1.metric(
            "Pressure",
            f"{today['pressure']} hPa"
        )

        row2_col2.metric(
            "Cloud Cover",
            f"{today['cloud_cover']} %"
        )

        row2_col3.metric(
            "Rain",
            f"{today['precipitation']} mm"
        )

    category = today["category"]

    if category == "Good":
        st.success(f"🟢 {category}")
    elif category == "Moderate":
        st.warning(f"🟡 {category}")
    else:
        st.error(f"🔴 {category}")

    st.divider()
    st.subheader("📅 3-Day AQI Forecast")

    cols = st.columns(3)

    for forecast, col in zip(forecast_data, cols):

        with col:
            date_obj = datetime.strptime(
                forecast["date"],
                "%Y-%m-%d"
            )

            with st.container(border=True):

                st.markdown(
                    f"### {date_obj.strftime('%A')}\n\n"
                    f"**{date_obj.strftime('%d %b %Y')}**"
                )

                st.markdown(
                    f"# {forecast['predicted_aqi']:.0f}"
                )

                if forecast["category"] == "Good":
                    st.success(forecast["category"])
                elif forecast["category"] == "Moderate":
                    st.warning(forecast["category"])
                else:
                    st.error(forecast["category"])

                st.write(f"🌡 Temperature: {forecast['temperature']} °C")
                st.write(f"💧 Humidity: {forecast['humidity']} %")
                st.write(f"🌬 Wind Speed: {forecast['wind_speed']} km/h")

    st.divider()

    st.download_button(
        "📥 Download Forecast CSV",
        forecast_df.to_csv(index=False),
        "karachi_aqi_forecast.csv",
        "text/csv"
    )

elif page == "Analytics":

    st.subheader("📊 Exploratory Data Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(
            "correlation_heatmap.png",
            caption="Correlation Heatmap",
            use_container_width=True
        )

    with col2:
        st.image(
            "feature_importance.png",
            caption="Feature Importance",
            use_container_width=True
        )

    with col3:
        st.image(
            "aqi_distribution.png",
            caption="AQI Distribution",
            use_container_width=True
        )

    st.divider()

    st.subheader("📈 AQI Forecast Trend")

    chart_df = forecast_df[["date", "predicted_aqi"]].set_index("date")
    st.line_chart(chart_df)

    st.divider()

    st.subheader("📋 Forecast Dataset")
    st.dataframe(forecast_df, use_container_width=True)

elif page == "Model":

    st.subheader("🤖 Model Performance & Details")

    col1, col2, col3 = st.columns(3)

    col1.metric("R² Score", "0.97")
    col2.metric("RMSE", "2.06")
    col3.metric("MAE", "1.63")

    st.divider()

    st.write("**Model:** Linear Regression")
    st.write("**Forecast Horizon:** 3 Days")
    st.write("**Feature Store:** Hopsworks")
    st.write("**Model Registry:** Hopsworks")

elif page == "System Info":

    st.subheader("ℹ️ System Information")

    st.markdown("""
- Data Source: Open-Meteo Forecast API
- Prediction Model: Linear Regression
- Feature Store: Hopsworks
- Model Registry: Hopsworks
- Forecast Horizon: 3 Days

Built using FastAPI, Streamlit, Scikit-Learn and Hopsworks.
""")
