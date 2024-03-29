from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import *
# from phonenumber_field.modelfields import PhoneNumberField
tzname = datetime.now().astimezone().tzname()
class User(AbstractUser):
    card_num = models.PositiveBigIntegerField(default=0000)
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=16, default=" ")
    park_id = models.CharField(default='', max_length=100)
    car_num = models.CharField(max_length=12, default='')
    is_superadmin = models.BooleanField(default=False)
    parking_control = models.BooleanField(default=False)
    barrier_control = models.BooleanField(default=False)
    coupon_control = models.BooleanField(default=False)
    export_right = models.BooleanField(default=False)
    parking_lot_view = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.username} | user control {self.is_superadmin} | park control {self.parking_control} | barr control {self.barrier_control} | coupon_control {self.coupon_control} | admin_view {self.export_right}'
    

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
    reg_num = models.CharField(default='', max_length=100)

    def __str__(self) -> str:
        return f'{self.lattitude} | {self.longitude} | {self.reg_num} | {self.address} | {self.max_parking_lots} | {self.occupied_lots} | {self.price_per_hour} ||| '

class Reciept(models.Model):
    parking_id = models.CharField(default='', max_length=100)
    user_id = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    final_start_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    finish_time = models.DateTimeField(default=datetime(2, 1, 1, 0, 0, 0, tzinfo=None))
    final_price = models.BigIntegerField(default=-1)
    benefit = models.BooleanField(default=False)
    price_per_hour = models.IntegerField(default=-1)