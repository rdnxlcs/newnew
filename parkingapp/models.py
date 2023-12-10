from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    card_num = models.PositiveBigIntegerField(default=0)
    card_period = models.PositiveIntegerField(default=0)
    card_cvv = models.PositiveIntegerField(default=0)
    rights = models.IntegerField(default=0)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    park_id = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.username} | {self.rights}'
    

class Parking(models.Model):
    lattitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    address = models.CharField(max_length=120, default='')
    registry_nubmer = models.PositiveIntegerField(default=0)
    max_parking_spaces = models.PositiveIntegerField(default=0)
    occupied_places = models.PositiveIntegerField(default=0)
    price_per_minute = models.PositiveIntegerField(default=0)
    free_time = models.PositiveIntegerField(default=15)

    def __str__(self) -> str:
        return f'{self.address} | {self.max_parking_spaces}'

class Reciept(models.Model):
    parking_id = models.ForeignKey(Parking, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=None)
    finish_time = models.DateTimeField(default=None)
    final_price = models.BigIntegerField(default=-1)
    benefit = models.BooleanField(default=False)