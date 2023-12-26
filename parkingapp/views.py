from django.contrib import auth
from parkingapp.models import *
from django.urls import reverse
from datetime import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import make_aware
from django.http import JsonResponse
import ymaps
import json

from parkingapp.forms import UserLoginForm, UserRegistrationForm, AdminRegistrationForm, CouponerRegistrationForm

def check_logged(request):
    #print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return True
    return False


def logout(request):
    auth.logout(request)
    return redirect(reverse('parkingapp:index'))


def index(request):
    if request.method == 'POST':
        if 'create_park' in request.POST:
            user = request.user
            park_id = int(request.POST.get('park_id'))
            try:
                parking = Parking.objects.get(pk=park_id)
                print(type(parking))
                if parking.occupied_places >= parking.max_parking_spaces:
                    return redirect(reverse('parkingapp:error'))
                else:
                    parking.occupied_places += 1
                    parking.save()
                    starttime = datetime.now()
                    Reciept.objects.create(parking_id=parking, user_id=user, start_time=starttime, finish_time=starttime)
            except:
                return redirect(reverse('parkingapp:error'))
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
            logged = False
            if request.user.pk:
                logged = True
            return render(request, 'endparking.html', {'reciept': reciept, 'logged': check_logged(request)})


    try:
        reciepts = Reciept.objects.filter(user_id=request.user, final_price=-1)
        parkings = []
        for el in Parking.objects.all():
            parkings.append(el.longitude)
            parkings.append(el.lattitude)
            parkings.append(el.pk)
            parkings.append(el.max_parking_spaces - el.occupied_places)
            parkings.append(el.price_per_minute)
            parkings.append(el.address)
            parkings.append(99999)
        parkings = ' '.join(list(map(str, parkings))[:-1])

    except:
        parkings = []
        reciepts = []
    # url='v1' (on default)
    # BASE_URL = 'https://static-maps.yandex.ru/v1'
    return render(request, 'index.html', {'parking': Parking.objects.all(), 'reciepts': reciepts, 'logged':check_logged(request), "parkings":parkings, 'logged':check_logged(request)})

def dont_have_access(request):
    return render(request, 'dont_have_access.html')


def sign(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            password1 = make_password(request.POST['password1'])
            created_form = form.save(commit=False)
            created_form.password1 = password1
            created_form.password2 = password1
            created_form.righs = 0
            created_form.save()

            return HttpResponseRedirect(reverse('parkingapp:enter'))
    else:
        form = UserRegistrationForm()

    context = {
        'logged': check_logged(request),
        'form': form,
    }
    return render(request, 'sign.html', context)

def enter(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            # print('hereherehere')
            form = UserLoginForm(data=request.POST)
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('parkingapp:index'))
            except:
                print('зуй')
    else:
        form = UserLoginForm()

    context = {
        'logged': check_logged(request),
        'form': form,
    }
    return render(request, 'enter.html', context)
    
def addparking(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        client = ymaps.Geocode('fe7387f0-4485-4341-91bd-7b6427f658d7')
        lat, lng = list(map(float, client.geocode(address)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()))

        max_parking_spaces = request.POST.get('max_parking_spaces')
        price_per_minute = 1
        occupied_places = 0
        Parking.objects.create(lattitude=lat, longitude=lng, address=address, max_parking_spaces=max_parking_spaces, occupied_places=occupied_places, price_per_minute=price_per_minute)
        return render(request, 'panel.html', {'logged':check_logged(request)})
    user = request.user
    if user.is_authenticated and user.rights == 2:
        return render(request, 'addparking.html', {'logged':check_logged(request)})
    else:
        return redirect(reverse('parkingapp:dont_have_access'))
    
def signadmin(request):
    current_user = request.user
    all_admins = User.objects.filter(rights=2)
    if current_user in all_admins:
        if request.method == 'POST':    
            form = AdminRegistrationForm(data=request.POST)
            password1 = make_password(request.POST['password1'])
            if form.is_valid():
                created_form = form.save(commit=False)
                created_form.password1 = password1
                created_form.rights = 2
                created_form.save()
                return HttpResponseRedirect(reverse('parkingapp:enter'))
        else:
            form = AdminRegistrationForm()

        context = {
            'logged': check_logged(request),
            'form': form
        }
        return render(request, 'signadmin.html', context)
    else:
        return HttpResponseRedirect(reverse('parkingapp:dont_have_access'))

def signcoupon(request):
    current_user = request.user
    all_admins = User.objects.filter(rights=2)
    if current_user in all_admins:
        if request.method == 'POST':    
            form = CouponerRegistrationForm(data=request.POST)
            password1 = make_password(request.POST['password1'])
            if form.is_valid():
                created_form = form.save(commit=False)
                created_form.password1 = password1
                created_form.rights = 1
                created_form.save()
                return HttpResponseRedirect(reverse('parkingapp:enter'))
        else:
            form = CouponerRegistrationForm()

        context = {
            'logged': check_logged(request),
            'form': form
        }
        return render(request, 'signcoupon.html', context)
    
    else:
        return HttpResponseRedirect(reverse('parkingapp:dont_have_access'))   
   

def coupon(request):
    user = request.user
    if user.is_authenticated and user.rights == 1:
        if request.method == 'POST':
            checkid = request.POST.get('benifit')
            reciept = Reciept.objects.get(pk=checkid)
            reciept.benefit = True
            reciept.save()
        
        return render(request, 'coupon.html', {'logged':check_logged(request)})
    else:
        return redirect(reverse('parkingapp:index'))


def endparking(request):
    return render(request, 'endparking.html', {'logged':check_logged(request)})


def esp(request):
    return render(request, 'esp.html', {'logged':check_logged(request)})


def error(request):
    return render(request, 'error.html', {'logged':check_logged})


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
    print(len(parkings))
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

                if minutes <= 15:
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
        else:
            total_time = 0
            min_session = 0
            max_session = 0
            benefits_session_avarage_duration = 0
            max_benefit_session = 0
            session_avarage_duration = 0


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

def abc(start_time, finish_time):
    #do shit 
    pass

def panel(request):
    user = request.user

    if user.is_authenticated and user.rights == 2:
        parkings = Parking.objects.all()

        if request.method == 'POST':

            period_start = request.POST.get('period_start')
            period_end = request.POST.get('period_end')

            parks, fins = data(period_start, period_end)

            context = {
                'parkings': parks,
                'fins': fins,
                'start':  str(period_start)[:10], 
                'end': str(period_end)[:10],
                'logged':check_logged(request)
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
            period_start = '2012-10-12'
            period_end = '2012-10-12'
            parks, fins = data(period_start, period_end)

        context = {
            'parkings': parks,
            'fins': fins,
            'start':  str(period_start)[:10], 
            'end': str(period_end)[:10],
            'logged':check_logged(request)
        }

        return render(request, 'panel.html', context)
    else: 
        return redirect(reverse('parkingapp:dont_have_access'))



def dash_full(request):
    return render(request, 'dash_full.html')

def dash_coupon(request):
    return render(request, 'dash_coupon.html')

def dash_fin(request):
    return render(request, 'dash_fin.html')

def dash_users(request):
    return render(request, 'dash_users.html')
def compare_parks(request):
    p_start = datetime(2022, 12, 25, 0, 0, 0, tzinfo=None)
    p_end = datetime(2024, 12, 25, 23, 59, 59, tzinfo=None)
    reciepts_to_send = {}
    reciepts_to_send["parks"] = {}
    parkings = Parking.objects.all()
    for park in parkings:
        reciepts = Reciept.objects.filter(parking_id=park.pk)
        for reciept in reciepts:
            print(park, reciept.start_time.day)
            dt = datetime(reciept.start_time.year, reciept.start_time.month, reciept.start_time.day, reciept.start_time.hour, reciept.start_time.minute, reciept.start_time.second, tzinfo=None)
            if p_end >= dt >= p_start:
                try:
                    reciepts_to_send['parks'][str(park.pk)] += 1
                except:
                    reciepts_to_send['parks'][str(park.pk)] = 1
    reciepts_to_send = str(reciepts_to_send)
    print(json.dumps(reciepts_to_send))
    return render(request, 'charts.html', {'reciepts': json.dumps(reciepts_to_send)})

def compare_time(request):
    p_start = datetime(2023, 12, 1, 0, 0, 0, tzinfo=None)
    p_end = datetime(2023, 12, 26, 23, 59, 59, tzinfo=None)
    if p_end - p_start <= timedelta(days=1):
        delta = timedelta(hours=1)
        ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
        reciepts_to_send = {}
        reciepts_to_send['name'] = 'часам'
        reciepts_to_send["period"] = {}
        reciepts = Reciept.objects.all()
        while p_start <= ctime <= p_end:
            reciepts_to_send["period"][str(ctime.hour)] = 0
            for el in reciepts:
                etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                if ctime <= etime <= ctime+delta:
                    reciepts_to_send["period"][str(ctime.hour)] += 1
            ctime += delta
        reciepts_to_send = str(reciepts_to_send)
        print(json.dumps(reciepts_to_send))
    elif timedelta(days=1) < p_end-p_start <= timedelta(days=90):
        print('here')
        delta = timedelta(days=1)
        ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
        reciepts_to_send = {}
        reciepts_to_send['name'] = 'дням'
        reciepts_to_send['period'] = {}
        reciepts = Reciept.objects.all()
        while p_start <= ctime <= p_end:
            reciepts_to_send['period'][str(ctime.day)] = 0
            for el in reciepts:
                etime = etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                if ctime <= etime <= ctime+delta:
                    reciepts_to_send['period'][str(ctime.day)] += 1
            ctime += delta
        reciepts_to_send = str(reciepts_to_send)
        print(json.dumps(reciepts_to_send))
        
    return render(request, 'charts.html', {'reciepts': json.dumps(reciepts_to_send)})

