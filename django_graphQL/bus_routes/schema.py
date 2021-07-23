import graphene
from .types import *


class Query(graphene.ObjectType):
    unique_stops = graphene.List(UniqueStopsType)
    all_bus_routes = graphene.List(BusRouteType)
    route_by_num = graphene.List(BusRouteType, route_num=graphene.String(required=True))
    route_by_stop = graphene.List(BusRouteType, stop_num=graphene.String(required=True))
    unique_routes = graphene.List(UniqueRoutesType)

    # returns a list of bus_route objects that have a matching route number
    def resolve_route_by_num(root, info, route_num):
        return_list = []
        for route in BusRoute.objects.all():
            if route.route_num == route_num:
                return_list.append(route)
        return return_list

    # returns a list of bus_route objects that have a matching stop number
    def resolve_route_by_stop(root, info, stop_num):
        return_list = []
        for route in BusRoute.objects.all():
            if route.stop_num == stop_num:
                return_list.append(route)
        return return_list

    def resolve_all_bus_routes(root, info):
        return BusRoute.objects.all()

    # return a list of unique bus routes
    def resolve_unique_routes(root, info):
        return UniqueRoutes.objects.all()

    # returns a list of unique bus stops
    def resolve_unique_stops(root, info):
        return UniqueStops.objects.all()


schema = graphene.Schema(
    query=Query
)

