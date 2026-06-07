# eda_report.py

import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("historical_aqi_dataset.csv")

profile = ProfileReport(
    df,
    title="Karachi AQI Analysis Report"
)

profile.to_file("eda_report.html")

print("EDA Report Generated")