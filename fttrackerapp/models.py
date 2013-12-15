from django.db import models

class FoodTruck(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=200)

class Location(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=200)

class Appearance(models.Model):
    def __unicode__(self):
        return str(self.truck)+" "+str(self.location)+" "+str(self.date)
    truck = models.ForeignKey(FoodTruck)
    location = models.ForeignKey(Location)
    date = models.DateTimeField('appearance day')

    class Meta:
        unique_together = ("truck", "location", "date")
