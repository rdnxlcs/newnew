# Generated by Django 5.0 on 2024-01-30 16:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("parkingapp", "0019_alter_parking_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parking",
            name="registry_nubmer",
        ),
    ]
