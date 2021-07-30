import requests
from .apikey import api_key


def weather_info():
    current_weather = {"temp": 0,
                       "feels_like": 0,
                       "pressure": 0,
                       "wind_speed": 0,
                       "weather": 0}

    forecast = requests.get(api_key)
    response = forecast.status_code
    if response != 200:
        print("Open Weather is not responding")
    else:
        forecast_data = forecast.json()

    i = forecast_data["current"]
    current_weather["temp"] = i["temp"]
    current_weather["feels_like"] = i["feels_like"]
    current_weather["pressure"] = i["pressure"]
    current_weather["wind_speed"] = i["wind_speed"]

    j = (i["weather"])
    j = (j[0])
    current_weather["weather"] = j["main"]
    return current_weather
