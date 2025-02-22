from django.db import models


class Point(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    extra_data = models.JSONField(default=dict, blank=True)  # Flexible JSON data for storing any data ex:address

    def __str__(self):
        return self.name


class Polygon(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.JSONField()
    extra_data = models.JSONField(default=dict, blank=True)  # Flexible JSON data for storing any data ex:density of population
    
    def __str__(self):
        return self.name
