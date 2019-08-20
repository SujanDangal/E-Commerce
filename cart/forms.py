from django import forms
from .models import *
from . models import Order

Countries = (
    ('1', 'Nepal'),
    ('2', 'India'),
    ('3', 'Bangladesh'),
)

State = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)


class OrderForm(forms.Form):
    f_name = forms.CharField(max_length=30, required=True)
    l_name = forms.CharField(max_length=30, required=True)
    company_name = forms.CharField(max_length=30, required=True)
    country = forms.ChoiceField(choices=Countries)
    street_add = forms.CharField(max_length=30, required=True)
    apartment = forms.CharField(max_length=30, required=False)
    town = forms.CharField(max_length=250, required=True)
    state = forms.ChoiceField(choices=State)
    postcode = forms.CharField(max_length=250, required=False)
    phone = forms.IntegerField(required=True)
    email = forms.EmailField(max_length=250, required=True)
    information = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Order
        fields = ('f_name', 'l_name', 'email', 'Company_name', 'Country', 'street_add', 'apartment', 'town', 'state',
                  'postcode', 'phone', 'email', 'information',)

