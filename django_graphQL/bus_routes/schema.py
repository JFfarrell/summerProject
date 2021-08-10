import graphene
from .types import *
from .weather import weather_parser
import pickle


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

        # for redundancy I will include atleast 10 times past the current day to allow wrap around
        extras = 0
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
          timeDep =  allDepartureTimes[x].split(':')
          departureTimeInSeconds = int(timeDep[0])*60*60 + int(timeDep[1])*60 + int(timeDep[2])
          travelTimeToStopInSeconds = (i/numStops)*position
          arrivalTimeInSeconds = (departureTimeInSeconds + travelTimeToStopInSeconds)

          arrivalSecond = int(arrivalTimeInSeconds % 60)
          remainder = arrivalTimeInSeconds // 60
          arrivalMinute = int(remainder % 60)
          arrivalHour = int(remainder // 60)

          arrivalTime = str(arrivalHour) + ":" + str(arrivalMinute) + ":" + str(arrivalSecond)
          x += 1
          if (x > len(allDepartureTimes)):
            x=0
          allArrivalTimes.append(arrivalTime)

        # get next x arriving buses, x being provided as "list_size"
        nextArrivalTimes = []
        for i in allArrivalTimes:
          if (int(hour) <= int(i.split(':')[0]) and len(nextArrivalTimes) < list_size):
            nextArrivalTimes.append(i)

        # return data
        return str(nextArrivalTimes)


schema = graphene.Schema(
    query=Query
)

