# Generated by Django 5.0 on 2023-12-26 01:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0004_remove_parking_last_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='last_changed',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]
