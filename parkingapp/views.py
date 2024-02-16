from django.contrib import auth
from parkingapp.models import *
from django.urls import reverse
from datetime import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.http import FileResponse
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.http import JsonResponse
import ymaps
import json
from parkingapp.forms import UserLoginForm, UserRegistrationForm, AdminRegistrationForm, CouponForm, DashForm, DashfinForm, ChangePriceForm, AddParkingForm, CommitParkingForm
import random
import pandas as pd


@login_required(redirect_field_name=None)
def index(request):
    form = CommitParkingForm()
    
    # if any([request.user.user_control, request.user.parking_control, request.user.barrier_control, request.user.coupon_control, request.user.admin_view, request.user.parking_lot_view]):
    #     return redirect(reverse('parkingapp:dont_have_access'))
    
    try:
        parkings = []
        for el in Parking.objects.all():
            parkings.append(el.longitude)
            parkings.append(el.lattitude)
            parkings.append(el.pk)
            parkings.append(el.max_parking_lots - el.occupied_lots)
            parkings.append(el.price_per_hour)
            parkings.append(el.max_parking_lots)
            parkings.append(el.address)
            parkings.append(99999)
        parkings = ' '.join(list(map(str, parkings))[:-1])
    except Exception as e:
        print(e)
        parkings = []
    
    try:
        bdsm = []
        reciepts = Reciept.objects.filter(user_id=request.user.pk, final_price=-1)
        for el in reciepts:
            parkingxd = Parking.objects.get(pk=el.parking_id)
            now = datetime.now().replace(tzinfo=None)
            t = el.start_time
            seconds = (now - t.replace(tzinfo=None)).total_seconds()
            minutes = int(seconds // 60)
            seconds -= minutes * 60
            seconds = int(seconds)
            price_per_minute = el.price_per_hour / 60
            if minutes <= 14:
                price_per_minute = 0
            bdsm.append([el, parkingxd.address, f'{minutes:02}', f'{seconds:02}', int(price_per_minute * minutes)])
    except Exception as e:
        print(e)
        reciepts = []
        bdsm = []
    
    context = {
        'title': 'Парковка',
        'reciepts': reciepts,  
        'parkings': parkings, 
        'bdsm': bdsm,
        'form': form,
        'error': ''
    }
    if request.method == 'POST':
        if 'create_park' in request.POST:
            form = CommitParkingForm(data=request.POST)
            if form.is_valid():
                user = request.user
                code = request.POST['code']
                try:
                    parking = Parking.objects.get(code=code)
                    if parking.occupied_lots >= parking.max_parking_lots:
                        form = CommitParkingForm()
                        context['error'] = 'Нет свободных мест'
                        context['form'] = form
                        return render(request, 'index.html', context)
                    else:
                        extremecode = str(random.randint(1000, 9999)) + f'{parking.pk:03}' # subscribe!!!
                        parking.code = extremecode
                        parking.occupied_lots += 1
                        parking.save()
                        starttime = datetime.now().replace(tzinfo=None)
                        park_price = parking.price_per_hour
                        Reciept.objects.create(parking_id=parking.pk, user_id=user.pk, start_time=starttime, finish_time=starttime, price_per_hour=park_price, final_start_time=starttime.replace(tzinfo=None))
                        return redirect(reverse('parkingapp:index'))
                except Exception as e:
                    print(e)
                    form = CommitParkingForm()
                    context['error'] = 'Не удалось припарковаться'
                    context['form'] = form
                    return render(request, 'index.html', context)
            else:
                context['error'] = 'Не удалось припарковаться'
        elif 'end_park' in request.POST:
            reciept_id = request.POST.get('end_park')
            reciept = Reciept.objects.get(pk=reciept_id)
            now = datetime.now().replace(tzinfo=None)
            reciept.finish_time = now
            reciept.save()
            dif = now - reciept.final_start_time.replace(tzinfo=None)

            dif = dif.total_seconds()
            minutes = dif // 60
            if minutes <= 15:
                reciept.final_price = 0
            else:
                reciept.final_price = minutes * reciept.price_per_hour // 60
            reciept.save()
            parking = Parking.objects.get(pk=reciept.parking_id)
            parking.occupied_lots -= 1
            parking.save()

            reciept = Reciept.objects.get(pk=reciept_id)
            logged = False
            
            bdsm = []

            seconds = (reciept.finish_time - reciept.start_time).total_seconds()
            minutes = int(seconds // 60)
            seconds -= minutes * 60
            seconds = int(seconds)

            parkingxd = Parking.objects.get(pk=reciept.parking_id)
            reciept.start_time = reciept.start_time.strftime('%d-%m-%y %H:%M')
            reciept.finish_time = reciept.finish_time.strftime('%d-%m-%y %H:%M')
            bdsm = [reciept, parkingxd.address, f'{minutes:02}', f'{seconds:02}']

            context = {
                'reciept': bdsm, 
                'title': 'Парковка завершена'
            }

            return render(request, 'endparking.html', context)

    print(context)
    return render(request, 'index.html', context)

def dont_have_access(request):
    context = {
        'title': 'У вас нет доступа на эту страницу :('
    }
    return render(request, 'dont_have_access.html', context)

def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('parkingapp:enter'))

@login_required(redirect_field_name=None)
def endparking(request):
    context = {
    }
    return render(request, 'endparking.html', context)

def sign(request):
    error = ''
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password2']:
            form = form.save()
            return HttpResponseRedirect(reverse('parkingapp:enter'))
        else:
            print(form.errors)
            error = 'Не удалось зарегистрироваться'
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'error': error
    }
    return render(request, 'sign.html', context)

def enter(request):
    error = ''
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if any([request.user.user_control, request.user.parking_control, request.user.barrier_control, request.user.coupon_control, request.user.admin_view, request.user.parking_lot_view]):
                    return HttpResponseRedirect(reverse('parkingapp:dash_full')) 
                else:
                    return HttpResponseRedirect(reverse('parkingapp:index')) 
        else:
            error = 'Не удалось войти'

    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'enter.html', context)

def address_valid_check(address):
    try:
        client = ymaps.Geocode('fe7387f0-4485-4341-91bd-7b6427f658d7')
        lat, lng = list(map(float, client.geocode(address)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()))
        return True
    except:
        return False

@login_required(redirect_field_name=None)
def addparking(request):
    error = ''
    form = AddParkingForm()

    if not request.user.parking_control:
        return redirect(reverse('parkingapp:dont_have_access'))
    
    if request.method == 'POST':
        form = AddParkingForm(data=request.POST)
        try:
            if form.is_valid() and address_valid_check(request.POST['address']):
                address = request.POST['address']
                client = ymaps.Geocode('fe7387f0-4485-4341-91bd-7b6427f658d7')
                lat, lng = list(map(float, client.geocode(address)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()))
                max_parking_lots = request.POST['max_parking_lots']
                price = request.POST['price']
                occupied_lots = 0
                alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-&!@$^*()'
                alph = list(alph)
                secret = ''.join(random.choices(alph, k=100))
                Parking.objects.create(lattitude=lat, longitude=lng, address=address, max_parking_lots=max_parking_lots, occupied_lots=occupied_lots, price_per_hour=price, secret=secret)
                park = Parking.objects.filter(secret=secret)[0]
                code = str(random.randint(1000, 9999)) + f'{park.pk:03}'
                park.code = code
                park.save()
                return redirect(reverse('parkingapp:dash_parks'))
            else:
                error = 'Не удалось добавить парковку'
        except Exception as e:
            print(e)
            error = 'Не удалось добавить парковку'

    context = {
        'form': form, 
        'error': error
    }
    return render(request, 'addparking.html', context)
    
@login_required(redirect_field_name=None)
def signadmin(request):
    error = ''
    if not request.user.user_control:
        return HttpResponseRedirect(reverse('parkingapp:dont_have_access'))
    
    if request.method == 'POST':    
        form = AdminRegistrationForm(data=request.POST)
        addresses = [tuple([park.pk, park.address]) for park in list(Parking.objects.all())]
        form.fields['park_id'].choices = tuple(addresses)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            return HttpResponseRedirect(reverse('parkingapp:dash_users'))
        else:
            error = 'Не удалось зарегистрировать пользователя'
        
    
    form = AdminRegistrationForm()
    addresses = [tuple([park.pk, park.address]) for park in list(Parking.objects.all())]
    form.fields['park_id'].choices = tuple(addresses)

    context = {
        'title': 'Регистрация администратора',
        'form': form,
        'error': error,
    }
    return render(request, 'signadmin.html', context)

@login_required(redirect_field_name=None)
def coupon(request):
    error = ''
    if not request.user.coupon_control:
        return redirect(reverse('parkingapp:dont_have_access'))
    
    if request.method == 'POST':
        form = CouponForm(data=request.POST)
        if form.is_valid():
            pk = request.POST['user_reciept_id']
            reciept = Reciept.objects.filter(pk=pk)
            if reciept and not reciept[0].benefit and reciept[0].final_price == -1:
                reciept = reciept[0]
                reciept.benefit = True
                reciept.final_start_time = datetime.now().replace(tzinfo=None)
                reciept.save()
                
                return HttpResponseRedirect(reverse('parkingapp:coupon'))
    else:
        if request.method == 'POST':
            form = CouponForm(data=request.POST)
            if form.is_valid():
                car_num = request.POST['car'].upper()
                # phone_number = request.POST['phone']
                user = User.objects.filter(car_num=car_num)
                # user = User.objects.filter(phone_number)
                if user:
                    user = user[0]
                    reciept = Reciept.objects.filter(user_id=user.pk, final_price=-1)
                    if reciept and not reciept[0].benefit and reciept[0].final_price == -1:
                        reciept = reciept[0]
                        reciept.benefit = True
                        reciept.final_start_time = datetime.now().replace(tzinfo=None)
                        reciept.save()
                        
                        return HttpResponseRedirect(reverse('parkingapp:coupon'))
                    else:
                        error = 'У пользователя нет чеков'

            else:
                error = 'Не удалось выдать льготу'

    form = CouponForm()
    
    context = {
        'title': 'Обнуление чеков',
        'form': form,
        'error': error
    }

    return render(request, 'coupon.html', context)

@login_required(redirect_field_name=None)
def barrier(request):
    if not request.user.barrier_control:
        return redirect(reverse('parkingapp:dont_have_access'))
    return render(request, 'barrier.html', {'parkings': Parking.objects.all()})

@login_required(redirect_field_name=None)
def dash_corr(request):
    if not request.user.admin_view:
        return redirect(reverse('parkingapp:dont_have_access'))

    users = User.objects.all()
    corr_users = []
    corr_reciepts = []

    for user in users:
        user_reciepts = Reciept.objects.filter(user_id=user.pk)
        counter = 0
        for rec in user_reciepts:
            delta_hz = (rec.finish_time-rec.start_time)
            delta = delta_hz.days * 24 + delta_hz.seconds / 3600
            if rec.benefit and delta > 6:
                counter += 1
                corr_reciepts.append(rec)
                if counter >= 2:
                    corr_users.append(user)
                    corr_reciepts.append(rec)
                else:
                    del corr_reciepts[-1]
    
    context = {
        'corr_users': corr_users,
        'corr_reciepts': corr_reciepts
    }        

    return render(request, 'dash_corr.html', context)
    
def convert_data(DB):
    res = DB[0].__dict__
    for i in res:
        res[i] = []
        for row in DB:
            res[i].append(getattr(row, i))
    return res

@login_required(redirect_field_name=None)       
def export(request):
    df = pd.DataFrame(convert_data(Parking.objects.all()))
    df.to_excel('parkingapp/static/data.xlsx', index=False)
    return FileResponse(open('parkingapp/static/data.xlsx', 'rb'))

@login_required(redirect_field_name=None)
def profile(request):
    reciept = Reciept.objects.filter(user_id=request.user.pk)

    bdsm = []

    for rec in reciept:
        rec.start_time = rec.start_time.strftime('%d-%m-%y %H:%M')
        rec.finish_time = rec.finish_time.strftime('%d-%m-%y %H:%M')
        bdsm.append([rec, Parking.objects.get(pk=rec.parking_id).address])

    print(type(bdsm[0][0].start_time))
    

    print(User.objects.filter(pk=request.user.pk)[0])
    context = {
        'user': User.objects.filter(pk=request.user.pk)[0], 
        'bdsm': bdsm
    }
    if any([request.user.user_control, request.user.parking_control, request.user.barrier_control, request.user.coupon_control, request.user.admin_view, request.user.parking_lot_view]):
        return redirect(reverse('parkingapp:dash_profile'))
    else:
        return render(request, 'profile.html', context)

@login_required(redirect_field_name=None)
def dash_profile(request):
    context = {
        'user': User.objects.filter(pk=request.user.pk)[0], 
    }
    if any([request.user.user_control, request.user.parking_control, request.user.barrier_control, request.user.coupon_control, request.user.admin_view, request.user.parking_lot_view]):
        return render(request, 'dash_profile.html', context)
    else: 
        return redirect(reverse('parkingapp:profile'))

class Park: 
    def __init__(
                self, address, how_much_people_used, people_used_free_time,
                total_time, session_average_duration, min_session, max_session, 
                with_benefits, benefits_session_average_duration, max_benefit_session, total_benefit_time, total_sum, benefit_sum
            ) -> None:
        self.address = address
        self.how_much_people_used = how_much_people_used
        self.people_used_free_time = people_used_free_time
        self.total_time = total_time
        self.session_average_duration = session_average_duration
        self.min_session = min_session
        self.max_session = max_session
        self.with_benefits = with_benefits
        self.benefits_session_average_duration = benefits_session_average_duration
        self.max_benefit_session = max_benefit_session
        self.total_benefit_time = total_benefit_time
        self.total_sum = total_sum
        self.benefit_sum = benefit_sum
    
class Fin:
    def __init__(
            self, total_price, how_much_people_used, 
            with_benefits, benefits_price
        ) -> None:
        self.total_price = total_price
        self.how_much_people_used = how_much_people_used
        self.with_benefits = with_benefits
        self.benefits_price = benefits_price

def data(period_start, period_end, id=0):
    period_start = [i for i in period_start.split('-')]
    period_end = [i for i in period_end.split('-')]

    period_start = datetime( int(period_start[0]), int(period_start[1]), int(period_start[2]) , 0, 0, 0, tzinfo=None)
    period_end = datetime( int(period_end[0]), int(period_end[1]), int(period_end[2]), 23, 59, 59, tzinfo=None)
    
    if id:
        parkings = Parking.objects.filter(pk=id)
    else:
        parkings = Parking.objects.all()

    parkings_array = []
    fins_parkings_array = []
    for parking in parkings:
        reciepts = Reciept.objects.filter(parking_id=parking.pk)
        how_much_people_used = 0
        people_used_free_time = 0
        minutes = 0
        sessions = []
        benefit_sessions = []   
        with_benefits = 0
        prices = []
        benefit_prices = []
        for reciept in reciepts:
            if reciept.start_time.replace(tzinfo=None) >= period_start.replace(tzinfo=None) and reciept.finish_time.replace(tzinfo=None) <= period_end.replace(tzinfo=None):
                parking = Parking.objects.get(pk=reciept.parking_id)

                how_much_people_used += 1

                difference = (reciept.finish_time - reciept.start_time)
                benefit_difference = (reciept.finish_time - reciept.final_start_time)
                seconds = difference.total_seconds()
                benefit_minutes = benefit_difference.total_seconds() // 60
                minutes = seconds // 60

                sessions.append(minutes)
                prices.append(reciept.final_price)
                if reciept.benefit:
                    if minutes > 15:
                        benefit_prices.append(max(0 , minutes * reciept.price_per_hour - benefit_minutes * reciept.price_per_hour) / 60)
                    benefit_sessions.append(minutes)
                    with_benefits += 1
                if minutes <= 15:
                    people_used_free_time += 1
        if len(sessions) != 0:
            session_average_duration = int(sum(sessions)) // len(sessions)
            total_time = int(sum(sessions))
            total_benefit_time = int(sum(benefit_sessions))
            min_session = min(sessions)
            max_session = max(sessions)
            total_sum = sum(prices)
            if len(benefit_sessions) != 0:
                benefit_sum = sum(benefit_prices)
                benefits_session_average_duration = total_benefit_time // len(benefit_sessions)
                max_benefit_session = int(max(benefit_sessions))
            else:
                benefits_session_average_duration = 0
                max_benefit_session = 0
                benefit_sum = 0
        else:
            benefit_sum = 0
            total_time = 0
            total_sum = 0
            min_session = 0
            max_session = 0
            benefits_session_average_duration = 0
            max_benefit_session = 0
            total_benefit_time = 0
            session_average_duration = 0
            total_benefit_time = 0
        parkings_array.append(Park(
                parking.address, how_much_people_used, people_used_free_time, 
                total_time, session_average_duration, min_session, max_session, 
                with_benefits, benefits_session_average_duration, max_benefit_session, total_benefit_time=total_benefit_time, total_sum=int(total_sum), benefit_sum=int(benefit_sum)
            ))
    total_price = 0
    benefits_price = 0
    how_much_people_used = 0
    benefits_price = 0
    total_with_benefits = 0
    for park in parkings_array:
        total_price += park.total_sum
        how_much_people_used += park.how_much_people_used
        with_benefits = park.with_benefits
        total_with_benefits += with_benefits
        benefits_price += park.benefit_sum
    fins_parkings_array.append(
        Fin(
            total_price, how_much_people_used, 
            with_benefits=total_with_benefits, benefits_price=benefits_price
            )
    )
        
    return parkings_array, fins_parkings_array

def spice(p_end, p_start, period_start, period_end, pk, form, park, error):
    if p_end - p_start <= timedelta(days=1):
        delta = timedelta(hours=1)
        ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
        reciepts_to_send = {}
        reciepts_to_send['name'] = 'часам'
        reciepts_to_send["period"] = {}
        reciepts_to_send['free-period'] = {}
        reciepts = Reciept.objects.all()
        while p_start <= ctime <= p_end:
            reciepts_to_send["period"][str(ctime.hour)+'-'+str(ctime.day)] = 0
            reciepts_to_send['free-period'][str(ctime.hour)+'-'+str(ctime.day)] = 0
            for el in reciepts:
                etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                if ctime <= etime <= ctime+delta and el.finish_time - el.start_time > timedelta(minutes=15):
                    reciepts_to_send["period"][str(ctime.hour)+'-'+str(ctime.day)] += 1
                elif ctime <= etime <= ctime+delta and el.finish_time - el.start_time <= timedelta(minutes=15):
                    reciepts_to_send["period"][str(ctime.hour)+'-'+str(ctime.day)] += 1
            ctime += delta
        reciepts_to_send = str(reciepts_to_send)
    elif timedelta(days=1) < p_end-p_start <= timedelta(days=90):
        delta = timedelta(days=1)
        ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
        reciepts_to_send = {}
        reciepts_to_send['name'] = 'дням'
        reciepts_to_send['period'] = {}
        reciepts_to_send['free-period'] = {}
        reciepts = Reciept.objects.all()
        while p_start <= ctime <= p_end:
            reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
            reciepts_to_send['free-period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
            
            for el in reciepts:
                etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                if ctime <= etime <= ctime+delta and el.finish_time - el.start_time > timedelta(minutes=15):
                    reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
                elif ctime <= etime <= ctime+delta and el.finish_time - el.start_time <= timedelta(minutes=15):
                    reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
            ctime += delta
        reciepts_to_send = str(reciepts_to_send) 
    elif timedelta(days=90) < p_end-p_start:
        delta = timedelta(days=7)
        ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
        reciepts_to_send = {}
        reciepts_to_send['name'] = 'неделям'
        reciepts_to_send['period'] = {}
        reciepts_to_send['free_period'] = {}
        reciepts = Reciept.objects.all()
        week = 1
        while p_start <= ctime <= p_end:
            reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
            reciepts_to_send['free-period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
            
            for el in reciepts:
                etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                if ctime <= etime <= ctime+delta and el.finish_time - el.start_time > timedelta(minutes=15):
                    reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
                elif ctime <= etime <= ctime+delta and el.finish_time - el.start_time <= timedelta(minutes=15):
                    reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
            
            ctime += delta
            week += 1
        reciepts_to_send = str(reciepts_to_send)
    context = {'total_time': park.total_time,
            'average_time': park.session_average_duration,
            'total_benefit_time': park.total_benefit_time,
            'average_benefits': park.benefits_session_average_duration,
            'reciepts': json.dumps(str(reciepts_to_send)),
            'reciepts_benefit': json.dumps(str(coupon_reciepts(pk, period_start, period_end))),
            'form': form,
            'pk': pk,
            'error': error}
    return context

@login_required(redirect_field_name=None)
def dash_full(request):
    error = ''

    if not request.user.admin_view: 
        return redirect(reverse('parkingapp:dont_have_access'))
    
    if request.method == 'POST':
        form = DashForm(data=request.POST)
        addresses = [tuple([park.pk, park.address]) for park in list(Parking.objects.all())]
        form.fields['pk'].choices = tuple(addresses)
        if form.is_valid():
            pk = request.POST['pk']
            period_start = request.POST['date1']
            period_end = request.POST['date2']
            try:
                park = data(period_start, period_end, pk)[0][0]
                # total_time average_time 
                period_start = [i for i in period_start.split('-')]
                period_end = [i for i in period_end.split('-')]
                p_start = datetime( int(period_start[0]), int(period_start[1]), int(period_start[2]) , 0, 0, 0, tzinfo=None)
                p_end = datetime( int(period_end[0]), int(period_end[1]), int(period_end[2]), 23, 59, 59, tzinfo=None)
                context = spice(p_end, p_start, period_start, period_end, pk, form, park, error)
                return render(request, 'dash_full.html', context)
            except Exception as e:
                print(e)
                error = 'Неизвестная ошибка'
        else:
            error = 'Неверные входные данные'
        
    form = DashForm()
    addresses = [tuple([park.pk, park.address]) for park in list(Parking.objects.all())]
    form.fields['pk'].choices = tuple(addresses)
    pk = list(Parking.objects.all())[-1].pk 
    period_start = '2024-01-25'
    period_end = '2024-02-05'
    try:
        park = data(period_start, period_end, pk)[0][0]
        # total_time average_time 
        period_start = [i for i in period_start.split('-')]
        period_end = [i for i in period_end.split('-')]
        p_start = datetime( int(period_start[0]), int(period_start[1]), int(period_start[2]) , 0, 0, 0, tzinfo=None)
        p_end = datetime( int(period_end[0]), int(period_end[1]), int(period_end[2]), 23, 59, 59, tzinfo=None)
        context = spice(p_end, p_start, period_start, period_end, pk, form, park, error)
        return render(request, 'dash_full.html', context)
    except Exception as e:
        print(e)
        return render(request, 'dash_full.html', {'error': error})
    
@login_required(redirect_field_name=None)
def dash_parks(request):
    form = ChangePriceForm()        
    parkings = Parking.objects.all()
    error = ''

    if not request.user.parking_control: 
        return redirect(reverse('parkingapp:dont_have_access'))
    
    if request.method == 'POST':
        if 'change_price' in request.POST:
            form = ChangePriceForm(data=request.POST)
            if form.is_valid():
                pk = request.POST.get('change_price')
                new_price = request.POST['newprice']
                parking = Parking.objects.get(pk=pk)
                now = datetime.now().replace(tzinfo=None)
                tm = datetime(parking.change.year, parking.change.month, parking.change.day, parking.change.hour, parking.change.minute, parking.change.second, tzinfo=None)
                if now - tm >= timedelta(days=90):
                    parking.price_per_hour = new_price
                    parking.change = now
                    parking.save()
                    form = ChangePriceForm()
                else:
                    error = 'Изменение цены доступно раз в три месяца'
            else:
                error = 'Неверные входные данные'
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            parking = Parking.objects.get(pk=pk)
            parking.delete()
            form = ChangePriceForm()

    context = {
        'parkings': parkings, 
       'form': form, 
       'error': error
    }
    return render(request, 'dash_parks.html', context)

def coupon_reciepts(pk, period_start, period_end):
    try:
        parkingtest = Parking.objects.get(pk=pk)
        p_start = datetime( int(period_start[0]), int(period_start[1]), int(period_start[2]) , 0, 0, 0, tzinfo=None)
        p_end = datetime( int(period_end[0]), int(period_end[1]), int(period_end[2]), 23, 59, 59, tzinfo=None)        
        if p_end - p_start <= timedelta(days=1):
            delta = timedelta(hours=1)
            ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
            reciepts_to_send = {}
            reciepts_to_send['name'] = 'часам'
            reciepts_to_send["period"] = {}
            reciepts_to_send['free-period'] = {}
            reciepts = Reciept.objects.all()
            while p_start <= ctime <= p_end:
                reciepts_to_send["period"][str(ctime.hour)+'-'+str(ctime.day)] = 0
                for el in reciepts:
                    etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                    if ctime <= etime <= ctime+delta and el.benefit:
                        reciepts_to_send["period"][str(ctime.hour)+'-'+str(ctime.day)] += 1
                ctime += delta
            reciepts_to_send = str(reciepts_to_send)
        elif timedelta(days=1) < p_end-p_start <= timedelta(days=90):
            delta = timedelta(days=1)
            ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
            reciepts_to_send = {}
            reciepts_to_send['name'] = 'дням'
            reciepts_to_send['period'] = {}
            reciepts = Reciept.objects.all()
            while p_start <= ctime <= p_end:
                reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
                for el in reciepts:
                    etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                    if ctime <= etime <= ctime+delta and el.benefit:
                        reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
                ctime += delta
            reciepts_to_send = str(reciepts_to_send) 
        elif timedelta(days=90) < p_end-p_start:
            delta = timedelta(days=7)
            ctime = datetime(p_start.year, p_start.month, p_start.day, p_start.hour, p_start.minute, p_start.second, tzinfo=None)
            reciepts_to_send = {}
            reciepts_to_send['name'] = 'неделям'
            reciepts_to_send['period'] = {}
            reciepts = Reciept.objects.all()
            while p_start <= ctime <= p_end:
                reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
                reciepts_to_send['free-period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] = 0
                
                for el in reciepts:
                    etime = datetime(el.start_time.year, el.start_time.month, el.start_time.day, el.start_time.hour, el.start_time.minute, el.start_time.second, tzinfo=None)
                    if ctime <= etime <= ctime+delta and el.benefit:
                        reciepts_to_send['period'][str(ctime.day)+'.'+str(ctime.month)+'-'+str((ctime+delta).day)+'.'+str((ctime+delta).month)] += 1
                ctime += delta
            reciepts_to_send = str(reciepts_to_send)
        return reciepts_to_send
    except Exception as e:
        print(e)
        return ''

@login_required(redirect_field_name=None)
def dash_fin(request):
    form = DashfinForm()  
    period_start = '2024-01-25'
    period_end = '2024-02-05'
    dat = data(period_start, period_end)
    error = ''

    if not request.user.admin_view:
        return redirect(reverse('parkingapp:dont_have_access'))

    if request.method == 'POST':
        form = DashfinForm(data=request.POST)
        if form.is_valid():
            period_start = request.POST['date1']
            period_end = request.POST['date2']
            dat = data(period_start, period_end)
            context = {
                'Fin':dat[1][0],
                'parkings':dat[0],
                'form': form
            }
            return render(request, 'dash_fin.html', context)
        else:
            error = 'Неверные входные данные'

    
    context = {
        'Fin':dat[1][0],
        'parkings':dat[0],
        'form': form,
        'error': error
    }

    return render(request, 'dash_fin.html', context)

@login_required(redirect_field_name=None)
def dash_users(request):
    if not request.user.user_control:
        return redirect(reverse('parkingapp:dont_have_access'))

    if request.method == 'POST':
        value = request.POST.get('delete')
        user = User.objects.get(pk=value)
        user.delete()

    users = User.objects.all()

    context = {
        'title': '',
        'users': list(users),
    }
    return render(request, 'dash_users.html', context)

@login_required(redirect_field_name=None)
def dash_reciepts(request):
    if not request.user.admin_view:
        return redirect(reverse('parkingapp:dont_have_access'))
    
    reciepts = Reciept.objects.all()

    context = {
        'title': '',
        'reciepts': list(reciepts)[::-1],
    }
    return render(request, 'dash_reciepts.html', context)

@login_required(redirect_field_name=None)
def parking_lot(request):
    error = ''

    if not request.user.parking_lot_view:   
        return redirect(reverse('parkingapp:dont_have_access'))
    
    secret = request.GET.get('secret', '')
    if secret:
        try:
            parking = Parking.objects.filter(secret=secret)
            parking = parking[0]
            return render(request, 'parking_lot.html', {'parking': parking})
        except:
            parking = ''
            print(secret)
            error = 'Нет парковок'
    else:
        print(secret)
        parking = ''
        error = 'Нет ключа'
    
    return render(request, 'parking_lot.html', {'parking': parking, 'error': error})
