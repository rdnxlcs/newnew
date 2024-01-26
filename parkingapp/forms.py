from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from parkingapp.models import *


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
        'maxlength': 20,
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8,
        'maxlength': 100
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8,
        'maxlength': 100
    }))
    card = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер карты',
        'minlength': 4,
        'maxlength': 4,
        'inputmode': 'numeric',
    }))
    car = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Автомобильный номер',
        'minlength': 6,
        'maxlength': 12,
        'style': 'text-transform: uppercase;',
    }))
    tel = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер телефона',
        'id': 'tel',
        'inputmode': 'tel',
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'card', 'car', 'tel']


class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
        'maxlength': 20,
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CouponerRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
        'maxlength': 20,
    }))
    park_id = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'ID парковки',
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'park_id']


class CouponForm(forms.Form):
    user_reciept_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'id парковки для предоставления льготы',
        'inputmode': 'numeric'
    }))

    class Meta:
        model = Reciept
        fields = ['user_reciept_id']


class DashForm(forms.Form):
    pk = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control form-control-sm',
        'inputmode': 'numeric',
        'placeholder': 'id парковки',
    }))
    date1 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': '2023-12-09',
    }))
    date2 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': '2023-12-10',
    }))

class DashfinForm(forms.Form):
    date1 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': '2023-12-09',
    }))
    date2 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': '2023-12-10',
    }))

class ChangePriceForm(forms.Form):
    newprice = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': '',
        'placeholder': 'Новая цена',
        'style': "background: none; border: none"
    }))

class AddParkingForm(forms.Form):
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Адрес',
        'maxlength': 40
    }))
    max_parking_lots = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'id': 'a'
    }))
    price = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'id': 'a',
    }))



class CommitParkingForm(forms.Form):
    parking_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control group-first',
        'id': 'floatingInput',
        'inputmode': 'numeric',
        'placeholder': 'ID парковки',
    }))

    class Meta:
        model = Parking
        fields = ['parking_id']