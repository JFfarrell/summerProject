import graphene
from graphene_django import DjangoObjectType
from .models import BusRoute


class BusRouteType(DjangoObjectType):
    class Meta:
        model = BusRoute
        fields = ('id',
                  'StopSequence',
                  'RouteName',
                  'RouteDescription',
                  'Direction',
                  'AtcoCode',
                  'PlateCode',
                  'Latitude',
                  'Longitude',
                  'ShortCommonName_en',
                  'ShortCommonName_ga',
                  'HasPole',
                  'HasShelter',
                  'RouteData')


class Query(graphene.ObjectType):
    all_bus_routes = graphene.List(BusRouteType)

    def resolve_all_bus_routes(root, info):
        return BusRoute.objects.all()


schema = graphene.Schema(
    query=Query
)