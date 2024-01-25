from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import *

class User(AbstractUser):
    card_num = models.CharField(max_length=16, null=True, blank=True)
    card_period = models.CharField(max_length=4, null=True, blank=True)
    card_cvv = models.CharField(max_length=3, null=True, blank=True)
    rights = models.IntegerField(default=0, null=True)
    park_id = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.username} | {self.rights}'
    

class Parking(models.Model):
    lattitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=120, default='')
    registry_nubmer = models.PositiveIntegerField(default=0)
    max_parking_spaces = models.PositiveIntegerField(default=0)
    occupied_places = models.PositiveIntegerField(default=0)
    price_per_minute = models.PositiveIntegerField(default=0)
    change = models.DateTimeField(default=datetime(1, 1, 1, 0, 0, 0, tzinfo=None))

    def __str__(self) -> str:
        return f'{self.address} | {self.max_parking_spaces}'

class Reciept(models.Model):
    parking_id = models.ForeignKey(Parking, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=None)
    finish_time = models.DateTimeField(default=None)
    final_price = models.BigIntegerField(default=-1)
    benefit = models.BooleanField(default=False)