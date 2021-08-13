import datetime
import pytz
from .schema import *


def to_timestamp(time_in_seconds):
    arrival_second = str(int(time_in_seconds % 60))
    remainder = time_in_seconds // 60
    arrival_minute = str(int(remainder % 60))
    arrival_hour = str(int(remainder // 60))

    # eliminate single digits in timestamp
    if len(arrival_hour) == 1:
        arrival_hour = f"0{arrival_hour}"
    if len(arrival_minute) == 1:
        arrival_minute = f"0{arrival_minute}"
    if len(arrival_second) == 1:
        arrival_second = f"0{arrival_second}"
    arrival_time = arrival_hour + ":" + arrival_minute + ":" + arrival_second
    return arrival_time


def timestamp_to_seconds(time_list):
    ftr = [3600, 60, 1]
    times_in_seconds = []

    for time in time_list:
        time_units = time.split(':')
        total_secs = (int(time_units[0]) * ftr[2]) + (int(time_units[1]) * ftr[1]) + (int(time_units[0]) * ftr[0])
        times_in_seconds.append(total_secs)

    times_in_seconds.sort()
    return times_in_seconds


def departure_times(route, direction):
    timezone = pytz.timezone('Europe/Dublin')
    time_format = "%H:%M:%S"
    all_departure_times = []
    current = datetime.datetime.now(timezone).time()

    for unique_route in UniqueRoutes.objects.all():
        if unique_route.line_id == route and unique_route.direction == direction:
            dep_time = unique_route.first_departure_schedule.split(',')
            for time in dep_time:
                time = time.strip(" ")
                # preventing error thrown when time returned passes midnight
                time = correcting_midnight(time)

                time_stamp = datetime.datetime.strptime(time, time_format).time()
                if time_stamp > current:
                    all_departure_times.append(time)
    return all_departure_times


def travel_times(time, model, day, month):
    weather = weather_parser.weather_forecast()

    current_day = 0
    hour = time.split(":")[0].strip("0")
    key = str(current_day) + "-" + hour
    if key in weather:
        hourlyWeather = weather[key]
    else:
        current = "0-" + str(datetime.datetime.now().hour + 2)
        hourlyWeather = weather[current]

    rain = hourlyWeather["precip"]
    temp = hourlyWeather["temp"]
    return model.predict([[day, hour, month, rain, temp]])[0]


def data_and_direction(stop_num):
    data = []
    direction = ""

    for item in StopSequencing.objects.all():
        if item.stop_num == stop_num:
            data.append(item.stop_route_data)
            direction = item.direction

    return data, direction


def correcting_midnight(time):
    time_units = time.split(":")
    if int(time_units[0]) > 23:
        hour = int(time_units[0]) - 24
    else:
        hour = int(time_units[0])

    return str(hour) + ":" + time_units[1] + ":" + time_units[2]
