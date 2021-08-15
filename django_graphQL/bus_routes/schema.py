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

    stops_on_route = graphene.List(UniqueRoutesType,
                                   route_num=graphene.String(required=True),
                                   direction=graphene.String(required=True))

    stop_predictions = graphene.String(stop_num=graphene.String(required=True),
                                       day=graphene.String(required=True),
                                       #hour=graphene.String(required=True),
                                       month=graphene.String(required=True))

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

    def resolve_prediction(root, info, route, direction, day, hour, minute, month, list_size):
        # get relevant models pickle file
        model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl', 'rb'))

        # get all departure times
        all_departure_times = departure_times(route, direction)

        '''!!! issue here where our weather data only returns forecast data, so buses that have
        already departed don't have a corresponding weather object
        this shouldn't be too much of an issue as i will use the closest
        weather object, which will only be max 2 hrs off, but should revisit if have time'''
        # get all travel times
        all_travel_times = []
        for time in all_departure_times:
            all_travel_times.append(travel_times(time, model, day, month))

        # for redundancy I will include at least 10 times past the current day to allow wrap around
        # extras = 0
        # ----------------------------------------------------------------------------------------------------------
        # come back to this
        # ----------------------------------------------------------------------------------------------------------

        # predict each arrival time at chosen stop
        allStops = [x.strip() for x in Query.resolve_stops_on_route(root, info, route, direction).stops.split(",")]
        numStops = len(allStops)
        position = 0
        allArrivalTimes = {}
        for i in allStops:
          x = 0
          arrivalTimesForStop = []
          for j in all_travel_times:
            timeDep = all_departure_times[x].split(':')
            departureTimeInSeconds = int(timeDep[0])*60*60 + int(timeDep[1])*60 + int(timeDep[2])
            travelTimeToStopInSeconds = (j/numStops)*position
            arrivalTimeInSeconds = (departureTimeInSeconds + travelTimeToStopInSeconds)

            # convert num of seconds to time of day
            arrivalTime = to_timestamp(arrivalTimeInSeconds)

            x += 1
            if x > len(all_departure_times):
              x = 0

            arrivalTimesForStop.append(arrivalTime)

          allArrivalTimes[i] = arrivalTimesForStop
          position += 1

        # get next x arriving buses, x being provided as "list_size"
        nextArrivalTimes = {}
        for i in allArrivalTimes:
          nextTimes = []
          for j in allArrivalTimes[i]:
            if (int(hour) <= int(j.split(':')[0]) and len(nextTimes) < list_size):
              if (int(hour) == int(j.split(':')[0]) and int(minute) > int(j.split(':')[1])):
                pass
              else:
                nextTimes.append(j)
          nextArrivalTimes[i] = nextTimes

        # return data
        return str(nextArrivalTimes)

    def resolve_stop_predictions(self, info, stop_num, day, month):
        predictions = {}

        # get data and direction
        stop_data = data_and_direction(stop_num)

        for information in stop_data:
            print("information", information)
            info = information.split("_")
            route_num = info[0]
            divisor = float(info[1])
            direction = info[2]
            destination = info[3]

            exists = os.path.isfile(f'./bus_routes/route_models/{direction}/RandForest_{route_num}.pkl')
            if exists:
                # get all departure times for route
                all_departure_times = departure_times(route_num, direction)
                all_departure_times_in_seconds = timestamp_to_seconds(all_departure_times)

                # load appropriate model
                model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route_num}.pkl', 'rb'))
                print(all_departure_times)
                # current implementation is very slow, so limiting the output
                for time in all_departure_times:
                    prediction = travel_times(time, model, day, month)
                    prediction = int(prediction/divisor)
                    prediction = to_timestamp(prediction + all_departure_times_in_seconds[0])
                    predictions.update({route_num + "_" + destination + "_" + direction: prediction})
            else:
                pass

        return str(predictions)


schema = graphene.Schema(
    query=Query
)

