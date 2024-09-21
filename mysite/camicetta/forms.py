from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите email'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'delivery_type', 'address', 'comments']
        labels = {
            'first_name': '',
            'last_name': '',
            'phone': '',
            'delivery_type': '',
            'address': '',
            'comments': '',
        }

        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}),
            "last_name": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию'}),
            "phone": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите номер телефона'}),
            "address": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите адресс'}),
            "comments": forms.Textarea(attrs={'class': 'comments', 'placeholder': 'Введите комментарии к заказу'}),

        }


class LoadPhoto(forms.ModelForm):
    image = forms.FileField(label='Загрузить изоображение пользователя')
    class Meta:
        model = User
        fields = ['image']


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



