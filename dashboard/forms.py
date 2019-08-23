from django import forms
from django.utils import timezone
from .models import *
from acereadymade_app.models import *
from django.core.files.images import ImageFile


class AdminLogInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('username', 'passwords', )


class AddCategoryForm(forms.Form):
    name = forms.CharField(max_length=150)
    slug = forms.CharField(max_length=150)

    class Meta:
        fields = ('name', 'slug')


class AddProductForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField(max_length=150)
    slug = forms.SlugField(max_length=150)
    image = forms.ImageField()
    description = forms.CharField(max_length=500)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    stock = forms.IntegerField()
    available = forms.BooleanField(required=False)
    featured = forms.BooleanField(required=False)
    latest = forms.BooleanField(required=False)
    topkurtha = forms.BooleanField(required=False)
    topfeatured = forms.BooleanField(required=False)

class EditCategoryForm(forms.Form):
    name = forms.CharField(max_length=150)
    slug = forms.CharField(max_length=150)

    class Meta:
        fields = ('name', 'slug')





