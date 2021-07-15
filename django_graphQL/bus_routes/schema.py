import graphene
from graphene_django import DjangoObjectType
from .models import BusRoute


class BusRouteType(DjangoObjectType):
    class Meta:
        model = BusRoute
        fields = ('id',
                  'trip_id',
                  'shape_id',
                  'stop_id',
                  'stop_sequence',
                  'destination',
                  'stop_name',
                  'latitude',
                  'longitude',
                  'ainm',
                  'route_num',
                  'stop_num')


class Query(graphene.ObjectType):
    all_bus_routes = graphene.List(BusRouteType)
    unique_stops = graphene.List(BusRouteType)
    unique_routes = graphene.List(BusRouteType)
    route_by_num = graphene.List(BusRouteType, route_num=graphene.String(required=True))
    route_by_stop = graphene.List(BusRouteType, stop_num=graphene.String(required=True))

    # returns a list of unique bus stops
    def resolve_unique_stops(root, info):
      stops_list = []
      return_list = []
      for route in BusRoute.objects.all():
        if route.stop_num not in stops_list:
          stops_list.append(route.stop_num)
          return_list.append(route)
      return return_list

    # return a list of unique bus routes
    def resolve_unique_routes(root, info):
      route_list = []
      return_list = []
      for route in BusRoute.objects.all():
        if route.route_num not in route_list:
          route_list.append(route.route_num)
          return_list.append(route)
      return return_list

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


schema = graphene.Schema(query=Query)
