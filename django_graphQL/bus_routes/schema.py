import itertools
import graphene
from .types import *
from .weather import weather_parser
import pickle
import os
from .assistant_functions import *
import datetime
import warnings

warnings.filterwarnings("ignore")


class Query(graphene.ObjectType):
    prediction = graphene.String(route=graphene.String(required=True),
                                 direction=graphene.String(required=True),
                                 day=graphene.String(required=True),
                                 hour=graphene.String(required=True),
                                 minute=graphene.String(required=True),
                                 month=graphene.String(required=True),
                                 list_size=graphene.Int(required=True))

    stop_prediction_tom = graphene.String(stop_num=graphene.String(required=True),
                                          day=graphene.String(required=True),
                                          hour=graphene.String(required=True),
                                          minute=graphene.String(required=True),
                                          month=graphene.String(required=True),
                                          list_size=graphene.Int(required=True))

    stops_on_route = graphene.List(UniqueRoutesType,
                                   route_num=graphene.String(required=True),
                                   direction=graphene.String(required=True))

    unique_routes = graphene.List(UniqueRoutesType)

    stop_predictions = graphene.String(stop_num=graphene.String(required=True),
                                       day=graphene.String(required=True),
                                       hour=graphene.String(required=True),
                                       minute=graphene.String(required=True),
                                       month=graphene.String(required=True),
                                       list_size=graphene.Int(required=True))

    weather = graphene.String()
    unique_stops = graphene.List(UniqueStopsType)
    unique_routes = graphene.List(UniqueRoutesType)

    # return a list of unique bus routes
    def resolve_unique_routes(root, info):
        return UniqueRoutes.objects.all()

    # returns a list of unique bus stops
    def resolve_unique_stops(root, info):
        return UniqueStops.objects.all()

    def resolve_weather(root, info):
        weather_dict = weather_parser.weather_forecast()
        weather_dict = str(weather_dict)
        return weather_dict

    def resolve_stops_on_route(root, info, line_id, direction):
        for route in UniqueRoutes.objects.all():
            if route.line_id == line_id and route.direction == direction:
                return route

    def resolve_all_bus_routes(root, info):
        return BusRoute.objects.all()

    def resolve_prediction(root, info, route, direction, day, hour, minute, month, list_size):
        # get relevant models pickle file
        model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl', 'rb'))

        # get all departure times for route
        all_departure_times = []
        for i in UniqueRoutes.objects.all():
            if i.line_id == route and i.direction == direction:
                all_departure_times = [x.strip() for x in i.first_departure_schedule.split(',')]

        # get weather
        weather = weather_parser.weather_forecast()

        # get all travel times
        # !!! issue here where our weather data only returns forecast data, so buses that have already departed don't have a corresponding weather object
        # this shouldn't be too much of an issue as i will use the closest weather object, which will only be max 2 hrs off, but should revisit if have time
        all_travel_times = []
        current_day = 0
        for i in all_departure_times:
            hr = i.split(":")[0]
            key = str(current_day) + "-" + hr
            if key in weather:
                hourly_weather = weather[key]
            else:
                print(str(datetime.datetime.now()))
                hourly_weather = weather["0-" + str(datetime.datetime.now().hour + 1)]
            rain = hourly_weather["precip"]
            temp = hourly_weather["temp"]
            all_travel_times.append("0_" + str(model.predict([[day, hr, month, rain, temp]])[0]))

        # if number of stops listed is less than 'list_size', get stops from next day
        current_day = 1
        for i in all_departure_times:
            hr = i.split(":")[0]
            key = str(current_day) + "-" + hr
            hourly_weather = weather[key]
            rain = hourly_weather["precip"]
            temp = hourly_weather["temp"]
            all_travel_times.append("1_" + str(model.predict([[day, hr, month, rain, temp]])[0]))

        # predict each arrival time at chosen stop
        all_stops = [x.strip() for x in Query.resolve_stops_on_route(root, info, route, direction).stops.split(",")]
        num_stops = len(all_stops)
        position = 0
        all_arrival_times = {}
        for i in all_stops:
            x = 0
            arrival_times_for_stop = []
            for j in all_travel_times:
                day = j.split("_")[0]
                time = float(j.split("_")[1])
                time_dep = all_departure_times[x].split(':')
                departure_time_in_seconds = int(time_dep[0]) * 60 * 60 + int(time_dep[1]) * 60 + int(time_dep[2])
                travel_time_to_stop_in_seconds = (time / num_stops) * position
                arrival_time_in_seconds = (departure_time_in_seconds + travel_time_to_stop_in_seconds)

                arrival_second = str(int(arrival_time_in_seconds % 60))
                remainder = arrival_time_in_seconds // 60
                arrival_minute = str(int(remainder % 60))
                arrival_hour = str(int(remainder // 60))

                # eliminate single digits in timestamp
                if len(arrival_hour) == 1:
                    arrival_hour = f"0{arrival_hour}"
                if len(arrival_minute) == 1:
                    arrival_minute = f"0{arrival_minute}"
                if len(arrival_second) == 1:
                    arrival_second = f"0{arrival_second}"

                if day == "1":
                    arrival_time = arrival_hour + ":" + arrival_minute + ":" + arrival_second + " (tomorrow)"
                else:
                    arrival_time = arrival_hour + ":" + arrival_minute + ":" + arrival_second

                x += 1
                if x > len(all_departure_times) - 1:
                    x = 0

                arrival_times_for_stop.append(arrival_time)

            all_arrival_times[i] = arrival_times_for_stop
            position += 1

        # get next x arriving buses, x being provided as "list_size"
        next_arrival_times = return_arrival_times(all_arrival_times, hour, list_size, minute)

        # return data
        return str(next_arrival_times)

    def resolve_stop_predictions(self, info, stop_num, day, hour, minute, month, list_size):
        # get all routes through given stop
        routes = []
        characters = ["[", "]", "\\"]
        data = data_and_direction(stop_num)

        for information in data:
            for char in characters:
                information = information.replace(char, "")
            routes.append(information)

        # get relevant models pickle file
        models = return_models(routes)

        # get all departure times for each route through stop
        all_departure_times = return_departure_times(models)

        # get weather
        # we could choose to iterate over all the times and get weather predictions for all, but it seems wasteful...
        # let's take the current time for now
        rain = 0.5
        temp = 15
        # time = seconds_to_timestamp(unit_to_seconds(hour, minute))
        # weather = weather_parser.weather_forecast()
        # rain, temp = return_weather(weather, time, 0)

        # get a list of all predictions
        predictions = []
        predictions = predictions_list(all_departure_times, day, hour, minute, month, rain, temp, predictions, "today")

        if len(predictions) > 0:
            output = ordering_predictions(list_size, predictions)
            if len(output) < list_size:
                print("Looking to next day...")
                # time = seconds_to_timestamp(unit_to_seconds(6, 0))
                # rain, temp = return_weather(weather, time, 1)
                day = str(int(day)+1)
                tomorrow_predictions = predictions_list(all_departure_times, day, hour, minute, month, rain, temp, predictions, "tomorrow")
                for prediction in tomorrow_predictions:
                    predictions.append(prediction)
                output = ordering_predictions(list_size, predictions)
            output = ", ".join(str(elem) for elem in output[:list_size])
            return output

        return "No buses available."


schema = graphene.Schema(
    query=Query
)
