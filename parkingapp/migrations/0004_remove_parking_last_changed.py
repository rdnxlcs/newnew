# Generated by Django 5.0 on 2023-12-26 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0003_alter_user_password1_alter_user_password2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parking',
            name='last_changed',
        ),
    ]
