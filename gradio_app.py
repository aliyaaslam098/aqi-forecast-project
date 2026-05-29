import gradio as gr
import requests

# ==================================
# PREDICTION FUNCTION
# ==================================
def predict_aqi(
    temperature,
    humidity,
    wind_speed,
    aqi_lag_1,
    aqi_lag_2
):

    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            params={
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "aqi_lag_1": aqi_lag_1,
                "aqi_lag_2": aqi_lag_2
            }
        )

        result = response.json()

        return f"Predicted AQI: {result['predicted_aqi']}"

    except Exception as e:

        return f"Error: {str(e)}"


# ==================================
# GRADIO UI
# ==================================
demo = gr.Interface(
    fn=predict_aqi,

    inputs=[
        gr.Number(label="Temperature"),
        gr.Number(label="Humidity"),
        gr.Number(label="Wind Speed"),
        gr.Number(label="Previous AQI 1"),
        gr.Number(label="Previous AQI 2")
    ],

    outputs="text",

    title="AQI Prediction Dashboard",

    description="Enter weather conditions and previous AQI values to predict AQI."
)

# ==================================
# LAUNCH APP
# ==================================
demo.launch()