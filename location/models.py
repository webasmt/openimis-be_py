# location/models.py
from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HealthFacility(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class UserDistrict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.district_name}"
