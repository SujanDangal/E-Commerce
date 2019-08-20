from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django import forms
from datetime import date
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    email_confirmed = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Customer_details(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    user_info = models.CharField(max_length=150, null=True)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone_no = models.IntegerField()

    def __str__(self):
        return self.user_info


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    # description = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('acereadymade_app:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    latest = models.BooleanField(default=True)
    topkurtha = models.BooleanField(default=True)
    topfeatured = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("acereadymade_app:product_detail", args=[self.id, self.slug])

