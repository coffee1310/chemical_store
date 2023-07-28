from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *
class SearchForm(forms.Form):
    query = forms.CharField(label = '',max_length=100, widget=forms.TextInput(attrs={"class":"search-input",'placeholder': '',"name":"q"}))

class UserRegisterForm(forms.Form):
    username = forms.CharField(label="Никнейм", max_length=150, widget=forms.TextInput(attrs={"class":"username_input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class":"password_input"}))
    password2 = forms.CharField(label="Пароль (повторно)", widget=forms.PasswordInput(attrs={"class":"password_input"}))
    user_adress = forms.CharField(label="Адресс", max_length=255, widget=forms.TextInput(attrs={"class":"adress_input"}))
    user_birth_date = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={"class":"birth_day_input","id":"birth-input"}))

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Никнейм", max_length=150,widget=forms.TextInput(attrs={"class": "username_input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "password_input"}))

