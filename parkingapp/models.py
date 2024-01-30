from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import *
from dateutil import tz
# from phonenumber_field.modelfields import PhoneNumberField
tzname = datetime.now().astimezone().tzname()
class User(AbstractUser):
    card_num = models.PositiveBigIntegerField(default=1111)
    username = models.CharField(max_length=20, unique=True)
    password1 = models.CharField(max_length=200, default=" ")
    password2 = models.CharField(max_length=200, default=" ")
    phone_number = models.CharField(max_length=16, default=" ")
    park_id = models.IntegerField(default=0)
    car_num = models.CharField(max_length=12, default='')
    user_control = models.BooleanField(default=False)
    parking_control = models.BooleanField(default=False)
    barrier_control = models.BooleanField(default=False)
    coupon_control = models.BooleanField(default=False)
    admin_view = models.BooleanField(default=False)
    parking_lot_view = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f'{self.username} | user control {self.user_control} | park control {self.parking_control} | barr control {self.barrier_control} | coupon_control {self.coupon_control} | admin_view {self.admin_view}'
    

class Parking(models.Model):
    lattitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=120, default='')
    max_parking_lots = models.PositiveIntegerField(default=0)
    occupied_lots = models.PositiveIntegerField(default=0)
    price_per_hour = models.PositiveIntegerField(default=0)
    change = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    code = models.CharField(default='', max_length=10)
    secret = models.CharField(default='', max_length=100)

    def __str__(self) -> str:
        return f'{self.address} | {self.max_parking_lots}'

class Reciept(models.Model):
    parking_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    final_start_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    finish_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    final_price = models.BigIntegerField(default=-1)
    benefit = models.BooleanField(default=False)
    price_per_hour = models.IntegerField(default=-1)
    active = models.BooleanField(default=True)