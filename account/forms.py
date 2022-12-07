from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': "input__item"})
    )
    login = forms.CharField(
        max_length=50,
        unique=True,
        widget=forms.TextInput(attrs={'class': "input__item"})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': "input__item"})
    )
    password = forms.CharField(

    )