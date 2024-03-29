# Generated by Django 5.0 on 2024-02-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parkingapp", "0025_remove_user_password1_remove_user_password2"),
    ]

    operations = [
        migrations.AddField(
            model_name="parking",
            name="reg_num",
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name="user",
            name="card_num",
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
