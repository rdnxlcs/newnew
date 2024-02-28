from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from parkingapp.models import *
from parkingapp.global_variables import global_variables


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
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
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
    card_num = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер карты',
        'minlength': 4,
        'maxlength': 4,
        'inputmode': 'numeric',
    }))
    car_num = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Автомобильный номер',
        'minlength': 6,
        'maxlength': 12,
        'style': 'text-transform: uppercase;',
    }))
    phone_number = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер телефона',
        'id': 'tel',
        'inputmode': 'tel',
    }))
    class Meta:
        model = User
        fields = ['username', 'password', 'card_num', 'car_num', 'phone_number']
    password1 = forms.CharField(required=False)
class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
        'maxlength': 20,
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль',
        'minlength': 8
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Пароль ещё раз',
        'minlength': 8
    }))
    is_superadmin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'checkbox',
        'onclick': 'check()',
        'id': 'is_superadmin',
    }))
    parking_control = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'checkbox',
        'id': 'parking_control',
    }))
    barrier_control = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'checkbox',
        'id': 'barrier_control',
    }))
    coupon_control = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'onclick': 'temp()',
        'type': 'checkbox',
        'id': 'coupon_control',
    }))
    export_right = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'checkbox',
        'id': 'export_right',
    }))
    parking_lot_view = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'type': 'checkbox',
        'id': 'parking_lot',
        'disabled': 'true',
    }))
    park_id = forms.ChoiceField(required=False, choices=(), widget=forms.Select(attrs={
        'class': 'form-select rounded-4',
        'value': ''
    }))
    password1 = forms.CharField(required=False)
    user_control = forms.ChoiceField(required=False)
    admin_view = forms.ChoiceField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_superadmin', 'parking_control', 'barrier_control', 'coupon_control', 'export_right', 'parking_lot_view', 'park_id']
class CouponForm(forms.Form):
    car = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Автомобильный номер',
        'minlength': 6,
        'maxlength': 12,
        'id': 'uppercar',
        'style': 'text-transform: uppercase;',
    }))
    phone = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер телефона',
        'id': 'tel',
        'inputmode': 'tel',
    }))

    class Meta:
        model = Reciept
        fields = ['car', 'phone']

class DashForm(forms.Form):
    reg_num = forms.ChoiceField(required=True, choices=(), widget=forms.Select(attrs={
        'class': 'form-select form-select-sm',
        'value': '',
        'id': 'id_reg_num'
    }))
    date1 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': global_variables.default_start_time,
    }))
    date2 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': global_variables.default_end_time,
    }))

class DashfinForm(forms.Form):
    date1 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': global_variables.default_start_time,
    }))
    date2 = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control form-control-sm',
        'type': 'date',
        'style': 'background: none;',
        'value': global_variables.default_end_time,
    }))

class ChangePriceForm(forms.Form):
    newprice = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'id': 'fucksubmit',
        'placeholder': 'Новая цена',
        'class': 'form-control',
        'type': 'number',
        'inputmode': 'numeric',
    }))

class AddParkingForm(forms.Form):
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Адрес',
        'maxlength': 40
    }))
    max_parking_lots = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Места',
        'id': 'a'
    }))
    price = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Цена',
        'id': 'a',
    }))

class CommitParkingForm(forms.Form):
    code = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control group-first',
        'code': 'floatingInput',
        'inputmode': 'numeric',
        'placeholder': 'пошла нахуй блять'
    }))

    # class Meta:
    #     model = Parking
    #     fields = ['code']