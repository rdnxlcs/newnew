# Generated by Django 4.1.2 on 2023-12-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0003_parking_lattitude_parking_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='lattitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='parking',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
