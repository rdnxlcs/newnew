# Generated by Django 5.0 on 2024-01-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parkingapp", "0018_user_parking_lot_view"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parking",
            name="code",
            field=models.CharField(default="", max_length=10),
        ),
    ]
