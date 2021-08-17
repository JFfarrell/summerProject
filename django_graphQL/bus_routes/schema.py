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
        allDepartureTimes = []
        for i in UniqueRoutes.objects.all():
            if (i.line_id == route and i.direction == direction):
                allDepartureTimes = [x.strip() for x in i.first_departure_schedule.split(',')]

        # get weather
        weather = weather_parser.weather_forecast()

        # get all travel times
        # !!! issue here where our weather data only returns forecast data, so buses that have already departed don't have a corresponding weather object
        # this shouldn't be too much of an issue as i will use the closest weather object, which will only be max 2 hrs off, but should revisit if have time
        allTravelTimes = []
        currentDay = 0
        for i in allDepartureTimes:
            hr = i.split(":")[0]
            key = str(currentDay) + "-" + hr
            if key in weather:
                hourlyWeather = weather[key]
            else:
                hourlyWeather = weather["0-" + str(datetime.datetime.now().hour + 1)]
            rain = hourlyWeather["precip"]
            temp = hourlyWeather["temp"]
            allTravelTimes.append("0_" + str(model.predict([[day, hr, month, rain, temp]])[0]))

        # if number of stops listed is less than 'list_size', get stops from next day
        currentDay = 1
        for i in allDepartureTimes:
            hr = i.split(":")[0]
            key = str(currentDay) + "-" + hr
            hourlyWeather = weather[key]
            rain = hourlyWeather["precip"]
            temp = hourlyWeather["temp"]
            allTravelTimes.append("1_" + str(model.predict([[day, hr, month, rain, temp]])[0]))

        # predict each arrival time at chosen stop
        allStops = [x.strip() for x in Query.resolve_stops_on_route(root, info, route, direction).stops.split(",")]
        numStops = len(allStops)
        position = 0
        allArrivalTimes = {}
        for i in allStops:
            x = 0
            arrivalTimesForStop = []
            for j in allTravelTimes:
                day = j.split("_")[0]
                time = float(j.split("_")[1])
                timeDep = allDepartureTimes[x].split(':')
                departureTimeInSeconds = int(timeDep[0]) * 60 * 60 + int(timeDep[1]) * 60 + int(timeDep[2])
                travelTimeToStopInSeconds = (time / numStops) * position
                arrivalTimeInSeconds = (departureTimeInSeconds + travelTimeToStopInSeconds)

                arrivalSecond = str(int(arrivalTimeInSeconds % 60))
                remainder = arrivalTimeInSeconds // 60
                arrivalMinute = str(int(remainder % 60))
                arrivalHour = str(int(remainder // 60))

                # elimindate single digits in timestamp
                if len(arrivalHour) == 1:
                    arrivalHour = f"0{arrivalHour}"
                if len(arrivalMinute) == 1:
                    arrivalMinute = f"0{arrivalMinute}"
                if len(arrivalSecond) == 1:
                    arrivalSecond = f"0{arrivalSecond}"

                if day == "1":
                    arrivalTime = arrivalHour + ":" + arrivalMinute + ":" + arrivalSecond + " (tomorrow)"
                else:
                    arrivalTime = arrivalHour + ":" + arrivalMinute + ":" + arrivalSecond

                x += 1
                if x > len(allDepartureTimes) - 1:
                    x = 0

                arrivalTimesForStop.append(arrivalTime)

            allArrivalTimes[i] = arrivalTimesForStop
            position += 1

        # get next x arriving buses, x being provided as "list_size"
        nextArrivalTimes = {}
        for i in allArrivalTimes:
            nextTimes = []
            for j in allArrivalTimes[i]:
                if len(nextTimes) < list_size:
                    if len(j.split(':')[2]) == 2:
                        if int(hour) <= int(j.split(':')[0]):
                            if int(hour) == int(j.split(':')[0]) and int(minute) > int(j.split(':')[1]):
                                pass
                            else:
                                nextTimes.append(j)
                    else:
                        nextTimes.append(j)

            nextArrivalTimes[i] = nextTimes

        # return data
        return str(nextArrivalTimes)

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
        models = {}
        for i in routes:
            info = i.split("_")
            route = info[0]
            divisor = float(info[1])
            direction = info[2]
            destination = info[3]
            exists = os.path.isfile(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl')
            if exists:
                models[route + "_" + direction] = [pickle.load(open(f'.'
                                                                    f'/bus_routes/route_models'
                                                                    f'/{direction}/RandForest_{route}'
                                                                    f'.pkl', "rb")), destination, divisor]
            else:
                pass

        # get all departure times for each route through stop
        all_departure_times = {}
        for i in UniqueRoutes.objects.all():
            line_id = i.id
            for key, value in models.items():
                if key == line_id:
                    destination = value[1]
                    divisor = value[2]
                    key_string = f"{line_id}_{destination}_{divisor}"
                    all_departure_times[key_string] = [x.strip() for x in i.first_departure_schedule.split(',')]


        # get weather
        rain = 0.5
        temp = 15
        predictions = []

        # predict travel time for each routes departure to chosen stop
        for key, value in all_departure_times.items():
            route_info = key.split("_")
            route = str(route_info[0])
            direction = str(route_info[1])
            destination = str(route_info[2])
            new_key = route + "_" + direction + "_" + destination
            divisor = float(route_info[3])
            model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl', "rb"))
            prediction = model.predict([[day, 12, month, 0.5, 16]])[0]
            predicted_journey_time = prediction/divisor

            for item in value:
                time_units = item.split(":")
                item = unit_to_seconds(time_units[0], time_units[1])
                predicted_time = float(item + predicted_journey_time)
                cut_off_time = (int(hour) * 3600) + (int(minute) * 60)

                # assessment for times in the past
                if cut_off_time < predicted_time:
                    predictions.append(new_key + "_" + seconds_to_timestamp(predicted_time))
        
        if len(predictions) > 0:
            output = [predictions[0]]
            for value in range(list_size):
                for prediction in predictions:
                    prediction = prediction.replace("]", "")
                    prediction = prediction.replace("\\\\", "")
                    if prediction not in output:
                        temp_time = prediction.split("_")[-1]
                        for item in range(len(output)):
                            if prediction not in output:
                                check = output[item]
                                if temp_time < check.split("_")[-1]:
                                    output.insert(item, prediction)
                                elif len(output) <= list_size and item == len(output) - 1:
                                    output.append(prediction)

                output = ", ".join(str(elem) for elem in output[:list_size])
                return output

        return "No buses available."

    # def resolve_stop_predictions(self, info, stop_num, day, month, hour, minute, list_size):
    #     predictions = []
    #     # get data and direction
    #     stop_data = data_and_direction(stop_num)
    #
    #     for information in stop_data:
    #         info = information.split("_")
    #         route_num = info[0]
    #         divisor = float(info[1])
    #         direction = info[2]
    #         destination = info[3]
    #
    #         exists = os.path.isfile(f'./bus_routes/route_models/{direction}/RandForest_{route_num}.pkl')
    #         if exists:
    #             # get all departure times for route
    #             all_departure_times = departure_times(route_num, direction)
    #             all_departure_times_in_seconds = timestamp_to_seconds(all_departure_times)
    #
    #             # load appropriate model
    #             model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route_num}.pkl', 'rb'))
    #             counter = 0
    #             index = 0
    #             # for each time in our list we will return a prediction timestamp
    #             for time in all_departure_times:
    #                 user_input_time = unit_to_seconds(hour, minute)
    #                 timetable_time = unit_to_seconds(time.split(":")[0], time.split(":")[1])
    #                 #print(comparison_time, timetable_time)
    #                 # this comparison operator is implemented to reduce cut-off times, but limits the future output
    #                 if user_input_time < timetable_time + 1800:
    #                     #print(user_time, timetable_time + 1800)
    #                     prediction = predicted_travel_times(time, model, day, month)
    #                     prediction = int(prediction/divisor)
    #                     prediction = seconds_to_timestamp(prediction + all_departure_times_in_seconds[counter])
    #                     cut_off_time, prediction_time = user_time(hour, minute, prediction)
    #                     print(cut_off_time, prediction_time)
    #                     # assessment for times in the past
    #                     if cut_off_time < prediction_time:
    #                         predictions.append(f"{route_num}_{destination}_{direction}_{prediction}")
    #                     counter += 1
    #                 index += 1
    #
    #         else:
    #             pass
    #     #print(predictions)
    #     if len(predictions) > 0:
    #         output = [predictions[0]]
    #         for value in range(list_size):
    #             for prediction in predictions:
    #                 if prediction not in output:
    #                     prediction = prediction.replace("]", "")
    #                     prediction = prediction.replace("\\", "")
    #                     temp_time = prediction.split("_")[-1]
    #                     for item in range(len(output)):
    #                         if prediction not in output:
    #                             check = output[item]
    #                             if temp_time < check.split("_")[-1]:
    #                                 output.insert(item, prediction)
    #                             elif len(output) <= list_size and item == len(output) -1:
    #                                 output.append(prediction)
    #         return str(output[:list_size])
    #     else:
    #         return "No buses within next 90 minutes."


schema = graphene.Schema(
    query=Query
)
