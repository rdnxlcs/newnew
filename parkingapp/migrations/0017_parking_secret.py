# Generated by Django 5.0 on 2024-01-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parkingapp", "0016_remove_reciept_couponer_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="parking",
            name="secret",
            field=models.CharField(default="", max_length=100),
        ),
    ]
