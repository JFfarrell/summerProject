import requests
import apikey


def weatherinfo():
    cweather={"temp":0, "feels_like":0, "pressure":0, "wind_speed":0, "weather":0}
    forecast = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat=53.33306&lon=-6.24889&exclude=hourly,daily,minutely&appid={apikey.api}")
    response = forecast.status_code
    if response !=200:
        print("Open Weather is not responding")
    else:
        forecast_data = forecast.json()

    i = forecast_data["current"]
    cweather["temp"] = i["temp"]
    cweather["feels_like"] = i["feels_like"]
    cweather["pressure"] = i["pressure"]
    cweather["wind_speed"] = i["wind_speed"]
    j=(i["weather"])
    #for some reason "weather" is a list of one element, an element that is a dictionary
    j=(j[0])
    cweather["weather"]=j["main"]
    return(cweather)