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
                                 month=graphene.String(required=True),
                                 rain=graphene.String(required=True),
                                 temp=graphene.String(required=True),
                                 list_size=graphene.Int(required=True),
                                 stop_num=graphene.String(required=True))

    stops_on_route = graphene.List(UniqueRoutesType,
                                   route_num=graphene.String(required=True),
                                   direction=graphene.String(required=True))

    stop_predictions = graphene.String(stop_num=graphene.String(required=True),
                                       day=graphene.String(required=True),
                                       hour=graphene.String(required=True),
                                       month=graphene.String(required=True),
                                       rain=graphene.String(required=True),
                                       temp=graphene.String(required=True))

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
        weather_dict = weather_parser.weather_info()
        weather_dict = str(weather_dict)
        return weather_dict

    def resolve_stops_on_route(root, info, line_id, direction):
        for route in UniqueRoutes.objects.all():
          if route.line_id == line_id and route.direction == direction:
              return route

    def resolve_prediction(root, info, route, direction, day, hour, month, rain, temp, list_size, stop_num):
        
        # get relevant models pickle file
        model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl', 'rb'))

        # get all departure times for route
        allDepartureTimes = []
        for i in UniqueRoutes.objects.all():
          if (i.line_id == route and i.direction == direction):
            allDepartureTimes = [x.strip() for x in i.first_departure_schedule.split(',')]

        # get all travel times
        allTravelTimes = []
        for i in allDepartureTimes:
          hr = i.split(":")[0].strip("0")
          allTravelTimes.append(model.predict([[day, hr, month, rain, temp]])[0])

        # for redundancy I will include at least 10 times past the current day to allow wrap around
        # extras = 0
        # ----------------------------------------------------------------------------------------------------------
        # come back to this
        # ----------------------------------------------------------------------------------------------------------

        # predict each arrival time at chosen stop
        route_data = Query.resolve_stops_on_route(root, info, route, direction)
        allStops = [x.strip() for x in route_data.stops.split(",")]
        position = 0
        for i in allStops:
          if stop_num == i:
            break
          else:
            position += 1
        numStops = len(allStops)
        allArrivalTimes = []
        x = 0
        for i in allTravelTimes:
          timeDep = allDepartureTimes[x].split(':')
          departureTimeInSeconds = int(timeDep[0])*60*60 + int(timeDep[1])*60 + int(timeDep[2])
          travelTimeToStopInSeconds = (i/numStops)*position
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

          arrivalTime = arrivalHour + ":" + arrivalMinute + ":" + arrivalSecond

          x += 1
          if x > len(allDepartureTimes):
            x = 0
          allArrivalTimes.append(arrivalTime)

        # get next x arriving buses, x being provided as "list_size"
        nextArrivalTimes = []
        for i in allArrivalTimes:
          if (int(hour) <= int(i.split(':')[0]) and len(nextArrivalTimes) < list_size):
            nextArrivalTimes.append(i)

        # return data
        return str(nextArrivalTimes)

    def resolve_stop_predictions(self, info, stop_num, day, hour, month, rain, temp):
        predictions = {}
        data = []
        direction = ""

        format = "%H:%M:%S"
        for item in StopSequencing.objects.all():
            if item.stop_num == stop_num:
                data.append(item.stop_route_data)
                direction = item.direction
        for information in data:
            info = information.split(", ")
            for line in info:
                line_data = line.strip("[]").split(": ")
                route = line_data[0]
                print(route)
                divisor = float(line_data[1])
                exists = os.path.isfile(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl')
                if exists:
                    current = datetime.datetime.now().time()
                    print("current time: ", current)
                    # get all departure times for route
                    allDepartureTimes = []
                    for i in UniqueRoutes.objects.all():
                        if i.line_id == route and i.direction == direction:
                            dep_time = i.first_departure_schedule.split(',')
                            for time in dep_time:
                                time = time.strip(" ")
                                time_stamp = datetime.datetime.strptime(time, format).time()
                                if time_stamp > current:
                                    allDepartureTimes.append(time)

                    model = pickle.load(open(f'./bus_routes/route_models/{direction}/RandForest_{route}.pkl', 'rb'))
                    prediction = int(model.predict([[day, hour, month, rain, temp]])[0])
                    print(prediction)
                    prediction = int(prediction/divisor)
                    allDepartureTimes = timestamp_to_seconds(allDepartureTimes)
                    for time in allDepartureTimes:
                        print(to_timestamp(time))
                    prediction = to_timestamp(prediction + allDepartureTimes[0])
                    predictions.update({route + "_" + direction: prediction})
                else:
                    pass

        return str(predictions)


schema = graphene.Schema(
    query=Query
)

