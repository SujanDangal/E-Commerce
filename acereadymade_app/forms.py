from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import *
import datetime
from django.forms.utils import ErrorList
from django.contrib.auth.models import User



class CustomerSignupForm(UserCreationForm):
    # user_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    phone_no = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_no', 'password1', 'password2',)


class CustomerLogInForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'Password',)