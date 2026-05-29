import requests

API_KEY = "ba57b5a591714a8404a1f71b11f5acd1"
CITY = "Karachi"

forecast_url = (
    f"https://api.openweathermap.org/data/2.5/forecast"
    f"?q={CITY}&appid={API_KEY}&units=metric"
)

response = requests.get(forecast_url)

data = response.json()

print("\nFORECAST API RESPONSE")
print("====================================")
print(data)
print("====================================")

print("\nSTATUS CODE:", response.status_code)

# Check if API failed
if response.status_code != 200:
    print("\nERROR: API request failed")
    print("Message:", data.get("message"))
    exit()

# Check if list exists
if "list" not in data:
    print("\nERROR: 'list' key not found in API response")
    exit()

forecast_list = data["list"]

print("\n3-DAY WEATHER FORECAST")
print("====================================")

for item in forecast_list[:3]:
    date_time = item["dt_txt"]
    temperature = item["main"]["temp"]
    humidity = item["main"]["humidity"]
    weather = item["weather"][0]["description"]

    print(f"""
Date & Time : {date_time}
Temperature : {temperature} °C
Humidity    : {humidity}%
Weather     : {weather}
------------------------------------
""")