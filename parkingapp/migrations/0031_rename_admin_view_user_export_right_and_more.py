# Generated by Django 4.1.2 on 2024-02-28 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingapp', '0030_alter_user_car_num_alter_user_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='admin_view',
            new_name='export_right',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_control',
            new_name='is_superadmin',
        ),
    ]
