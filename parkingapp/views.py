from django.contrib import auth
from parkingapp.models import *
from django.urls import reverse
from datetime import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.utils.timezone import make_aware
import geocoder

def index(request):
    if request.method == 'POST':
        if 'create_park' in request.POST:
            user = request.user
            park_id = request.POST.get('park_id')
            parkings = Parking.objects.filter(pk=park_id)
            if parkings:
                parking = parkings[0]
                parking.occupied_places += 1
                parking.save()

                starttime = datetime.now()
                Reciept.objects.create(parking_id=parking, user_id=user, start_time=starttime, finish_time=starttime)
        elif 'end_park' in request.POST:
            reciept_id = request.POST.get('end_park')
            reciept = Reciept.objects.get(pk=reciept_id)

            reciept.finish_time = datetime.now()
            parking = Parking.objects.get(pk=reciept.parking_id.pk)
            parking.occupied_places -= 1
            parking.save()
            dif = (reciept.finish_time.replace(tzinfo=None) - reciept.start_time.replace(tzinfo=None))
            dif = dif.total_seconds()
            minutes = int(parking.price_per_minute * dif // 60)
            if minutes <= 15 or reciept.benefit == True:
                reciept.final_price = 0

            else:
                reciept.final_price = int(parking.price_per_minute * dif // 60)
            reciept.save()


            reciept = Reciept.objects.get(pk=reciept_id)
            return render(request, 'endparking.html', {'reciept': reciept})
    try:
        reciepts = Reciept.objects.filter(user_id=request.user, final_price=-1)

    except:
        reciepts = []
    return render(request, 'index.html', {'parking': Parking.objects.all(), 'reciepts': reciepts})

def create_parking(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        address = request.POST.get('address')
        max_parking_spaces = request.POST.get('max_parking_spaces')
        price_per_minute = 70
        occupied_places = 0
        Parking.objects.create(lattitude=lat, longitude=lng, address=address, max_parking_spaces=max_parking_spaces, occupied_places=occupied_places, price_per_minute=price_per_minute)
    return render(request, 'create_parking.html')

def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        card_num = request.POST.get('card_num')
        card_period = request.POST.get('card_period')
        card_cvv = request.POST.get('card_cvv')
        user_password = request.POST.get('user_password')
        try :
            User.objects.get(username=username)
        except:
            return render(request, 'sign.html', {'error': 'Такой пользователь уже существует!'})
        User.objects.create(username=username, card_num=card_num, card_period=card_period, card_cvv=card_cvv, password=user_password)
        return redirect(reverse('parkingapp:enter'))

    return render(request, 'sign.html')

def enter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('parkingapp:index'))
        except:
            return render(request, 'enter.html', {'error': 'ДУРА!!! ПОШЛА НАХУЙ!'})

    return render(request, 'enter.html')
    
def addparking(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        address = request.POST.get('address')
        max_parking_spaces = request.POST.get('max_parking_spaces')
        price_per_minute = 70
        occupied_places = 0
        Parking.objects.create(lattitude=lat, longitude=lng, address=address, max_parking_spaces=max_parking_spaces, occupied_places=occupied_places, price_per_minute=price_per_minute)
        return render(request, 'admin.html')

    return render(request, 'addparking.html')

def signadmin(request):
    if request.method == 'POST':
        user = request.user
        admins = User.objects.filter(rights=2)
        if user in admins:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try :
                User.objects.get(username=username)
            except:
                return render(request, 'signadmin.html', {'error': 'Такой пользователь уже существует!'})
            User.objects.create(username=username, password=password, rights=2)
            return HttpResponseRedirect(reverse('parkingapp:enter'))
        else:
            return render(request, 'error.html')
    return render(request, 'signadmin.html')

def signcoupon(request):
    if request.method == 'POST':
        user = request.user
        admins = User.objects.filter(rights=2)
        if user in admins:
            username = request.POST.get('username')
            password = request.POST.get('password')
            park_id = request.POST.get('park_id')
            try :
                User.objects.get(username=username)
            except:
                return render(request, 'signcoupon.html', {'error': 'Такой пользователь уже существует!'})
            User.objects.create(username=username, password=password, park_id=park_id, rights=1)
            return HttpResponseRedirect(reverse('parkingapp:enter'))
        else:
            return render(request, 'error.html')
    return render(request, 'signcoupon.html')
   

def coupon(request):
    user = request.user
    if user.rights == 1:
        if request.method == 'POST':
            checkid = request.POST.get('benifit')
            reciept = Reciept.objects.get(pk=checkid)
            reciept.benefit = True
            reciept.save()
        
        return render(request, 'coupon.html')
    else:
        return redirect(reverse('parkingapp:index'))


def endparking(request):
    return render(request, 'endparking.html')


def esp(request):
    if request.method == 'POST':
        auth.logout(request)
    return render(request, 'esp.html')


def error(request):
    return render(request, 'error.html')


class Park: 
    def __init__(
                self, address, how_much_people_used, people_used_free_time,
                total_time, session_avarage_duration, min_session, max_session, 
                with_benefits, benefits_session_avarage_duration, max_benefit_session
            ):
        self.address = address
        self.how_much_people_used = how_much_people_used
        self.people_used_free_time = people_used_free_time
        self.total_time = total_time
        self.session_avarage_duration = session_avarage_duration
        self.min_session = min_session
        self.max_session = max_session
        self.with_benefits = with_benefits
        self.benefits_session_avarage_duration = benefits_session_avarage_duration
        self.max_benefit_session = max_benefit_session

class Fin:
    def __init__(
            self, address, total_price, how_much_people_used, 
            with_benefits, benefits_price
        ):
        self.address = address
        self.total_price = total_price
        self.how_much_people_used = how_much_people_used
        self.with_benbefits = with_benefits
        self.benefits_price = benefits_price

def data(period_start, period_end):
    period_start = [i for i in period_start.split('-')]
    period_end = [i for i in period_end.split('-')]

    period_start = datetime( int(period_start[0]), int(period_start[1]), int(period_start[2]) , 0, 0, 0, tzinfo=timezone(timedelta(hours=0)))
    period_end = datetime( int(period_end[0]), int(period_end[1]), int(period_end[2]), 23, 59, 59, tzinfo=timezone(timedelta(hours=0)))

    parkings = Parking.objects.all()
    parkings_array = []
    fins_parkings_array = []
    for park in parkings:
        reciepts = Reciept.objects.filter(parking_id=park.pk)

        how_much_people_used = 0
        people_used_free_time = 0
        minutes = 0
        sessions = []
        benefit_sessions = []
        with_benefits = 0

        for reciept in reciepts:
            if reciept.start_time >= period_start and reciept.finish_time <= period_end:
                parking = reciept.parking_id
                parking_id = parking.pk

                how_much_people_used += 1

                difference = (reciept.finish_time - reciept.start_time)
                seconds = difference.total_seconds()
                minutes = seconds // 60

                sessions.append(minutes)

                if minutes <= parking.free_time:
                    people_used_free_time += 1

                if reciept.benefit == True:
                    with_benefits += 1
                    benefit_sessions.append(minutes)

        if len(sessions) != 0:
            session_avarage_duration = int(sum(sessions)) // len(sessions)
            total_time = int(sum(sessions))
            min_session = min(sessions)
            max_session = max(sessions)
            if len(benefit_sessions) != 0:
                benefits_session_avarage_duration = int(sum(benefit_sessions)) // len(benefit_sessions)
                max_benefit_session = int(max(benefit_sessions))
            else:
                benefits_session_avarage_duration = 0
                max_benefit_session = 0

        parkings_array.append(Park(
                park.address, how_much_people_used, people_used_free_time, 
                total_time, session_avarage_duration, min_session, max_session, 
                with_benefits, benefits_session_avarage_duration, max_benefit_session
            )) 
        
        for park in parkings_array:
            parking = Parking.objects.get(address=park.address)
            price_per_minute = parking.price_per_minute
            total_price = price_per_minute * minutes
            how_much_people_used = park.how_much_people_used
            with_benefits = park.with_benefits
            benefits_price = with_benefits * price_per_minute

            fins_parkings_array.append(
                Fin(
                    parking.address, total_price, how_much_people_used, 
                    with_benefits, benefits_price
                    )
            )

        return parkings_array, fins_parkings_array

def panel(request):
    user = request.user
    print(user)
    if user.rights == 2:
        parkings = Parking.objects.all()

        if request.method == 'POST':

            period_start = request.POST.get('period_start')
            period_end = request.POST.get('period_end')

            parks, fins = data(period_start, period_end)

            context = {
                'parkings': parks,
                'fins': fins,
                'start':  str(period_start)[:10], 
                'end': str(period_end)[:10]
            }

            rsn = render(request, 'panel.html', context)
            rsn.set_cookie('period_start', str(period_start)[:10])
            rsn.set_cookie('period_end', str(period_end)[:10])
            
            return rsn
        try:
            period_start = request.COOKIES['period_start']
            period_end = request.COOKIES['period_end']
            parks, fins = data(period_start, period_end)
        except:
            period_start = ''
            period_end = ''

        context = {
            'parkings': parks,
            'fins': fins,
            'start':  str(period_start)[:10], 
            'end': str(period_end)[:10]
        }

        return render(request, 'panel.html', context)
    else: 
        return redirect(reverse('parkingapp:index'))   