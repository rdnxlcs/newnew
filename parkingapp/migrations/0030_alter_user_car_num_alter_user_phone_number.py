# Generated by Django 4.1.2 on 2024-02-27 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0029_alter_user_park_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='car_num',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=' ', max_length=16),
        ),
    ]
