from django.db import models


class BusRoute(models.Model):
    id = models.CharField("id", max_length=100, primary_key=True)
    StopSequence = models.IntegerField("StopSequence")
    RouteName = models.CharField("RouteName", max_length=20)
    RouteDescription = models.CharField("RouteDescription", max_length=100)
    Direction = models.CharField("Direction", max_length=10)
    StopID = models.CharField("StopID", max_length=50)
    StopNum = models.CharField("StopNum", max_length=50)
    Latitude = models.FloatField("Latitude")
    Longitude = models.FloatField("Longitude")
    Name = models.CharField("Name", max_length=100)
    Ainm = models.CharField("Ainm", max_length=100)
    HasPole = models.CharField("HasPole", max_length=30)
    HasShelter = models.CharField("HasShelter", max_length=30)
    RouteData = models.CharField("RouteData", max_length=255)

    def __str__(self):
        return self.id
