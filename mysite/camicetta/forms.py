from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from .models import *


# class RegisterUserForm(UserCreationForm):
#     username = forms.TextInput(attrs={'class': 'form-input'})
#     email = forms.EmailInput(attrs={'class': 'form-input'})
#     first_name = forms.TextInput(attrs={'class': 'form-input'})
#     last_name = forms.TextInput(attrs={'class': 'form-input'})
#     password1 = forms.PasswordInput(attrs={'class': 'form-input'})
#     password2 =  forms.PasswordInput(attrs={'class': 'form-input'})

#     class Meta:
#         model = User
#         fileds = ("username", "email" , "first_name", "last_name" ,"password1", "password2")
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-input'}),
#             'email': forms.EmailInput(attrs={'class': 'form-input'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-input'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-input'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
#         }