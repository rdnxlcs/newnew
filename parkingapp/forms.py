from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from parkingapp.models import User


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
        'maxlenght': 20,
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
    card_num = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Номер карты',
        'minlength': 16,
        'maxlength': 16,
        'inputmode': 'numeric',
    }))
    card_period = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'Срок действия',
        'minlength': 4,
        'maxlength': 4,
        'inputmode': 'numeric',
    }))
    card_cvv = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'type': 'text',
        'class': 'form-control rounded-4',
        'placeholder': 'CVV код',
        'minlength': 3,
        'maxlength': 3,
        'inputmode': 'numeric',
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'card_num', 'card_period', 'card_cvv']


class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-4',
        'placeholder': 'Имя пользователя',
        'minlength': 4,
        'maxlenght': 20,
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
        'maxlenght': 20,
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