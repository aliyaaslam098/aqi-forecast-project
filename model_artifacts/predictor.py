import joblib
import pandas as pd

class Predictor:

    def __init__(self):
        self.model = joblib.load("aqi_forecast_model.pkl")

    def predict(self, inputs):
        df = pd.DataFrame(inputs)
        predictions = self.model.predict(df)

        return predictions.tolist()