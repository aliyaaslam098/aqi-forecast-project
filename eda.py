import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("historical_aqi_dataset.csv")

# =========================
# CORRELATION HEATMAP
# =========================

corr = df.corr(numeric_only=True)

plt.figure(figsize=(10, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title("Feature Correlation Matrix")

plt.tight_layout()

plt.savefig("correlation_heatmap.png")

plt.show()

