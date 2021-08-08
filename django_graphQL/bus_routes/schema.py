import graphene
from .types import *
from .weather import weather_parser
import pickle
from .live_data import live_api as live
from datetime import datetime
from .live_data import to_timestamp


class Query(graphene.ObjectType):
    prediction = graphene.String(route=graphene.String(required=True),
                                 direction=graphene.String(required=True),
                                 day=graphene.String(required=True),
                                 hour=graphene.String(required=True),
                                 month=graphene.String(required=True),
                                 rain=graphene.String(required=True),
                                 temp=graphene.String(required=True))

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

    def resolve_stops_on_route(root, info, route_num, direction):
        for route in UniqueRoutes.objects.all():
            if route.route_num == route_num and route.direction == direction:
                return route

    def resolve_prediction(root, info, route, direction, day, hour, month, rain, temp):
        # grab overall prediction time for route journey
        test = pickle.load(open(f'./bus_routes/route_models/inbound/RandForest_{route}.pkl', 'rb'))
        predicted_journey_time = test.predict([[day, hour, month, rain, temp]])

        # get the details of the requested route
        live_departures = live.live_data(route, direction)
        print(live_departures)
        route_data = Query.resolve_stops_on_route(root, info, route, direction)
        all_stops = route_data.stops.split(",")
        num_stops = len(all_stops)

        times = []
        for bus in live_departures:
            time = bus[0]
            ftr = [3600, 60, 1]
            dep_time_seconds = sum([a*b for a, b in zip(ftr, map(int, time.split(':')))])
            time_per_stop = predicted_journey_time/num_stops
            print(time_per_stop)

            temp = []
            for stop in range(len(all_stops)):
                predicted_arrival = dep_time_seconds + (time_per_stop * stop)
                predicted_time = to_timestamp.to_time(predicted_arrival)

                temp.append([all_stops[stop], predicted_time])
            times.append(temp)

        return str(times)


schema = graphene.Schema(
    query=Query
)

