# Generated by Django 4.2.5 on 2023-12-25 15:28

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('card_num', models.PositiveBigIntegerField(default=0)),
                ('card_period', models.PositiveIntegerField(default=0)),
                ('card_cvv', models.PositiveIntegerField(default=0)),
                ('rights', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password1', models.CharField(max_length=20)),
                ('park_id', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lattitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('address', models.CharField(default='', max_length=120)),
                ('registry_nubmer', models.PositiveIntegerField(default=0)),
                ('max_parking_spaces', models.PositiveIntegerField(default=0)),
                ('occupied_places', models.PositiveIntegerField(default=0)),
                ('price_per_minute', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=None)),
                ('finish_time', models.DateTimeField(default=None)),
                ('final_price', models.BigIntegerField(default=-1)),
                ('benefit', models.BooleanField(default=False)),
                ('parking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingapp.parking')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
