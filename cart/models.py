from django.db import models
from acereadymade_app.models import Product, User


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'Cart'  # defining the name of the table
        ordering = ['date_added']

    def __str__(self):
        return str(self.cart_id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # i.e if the product is deleted then any mention of that product is also deleted
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    quantity = models.IntegerField()
    price = models.DecimalField(blank=False, decimal_places=2, null=True, max_digits=15)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):  # to calculate the total price
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    Countries = (
        (1, 'Nepal'),
        (1, 'India'),
        (1, 'Bangladesh'),
    )
    State = (
        (1, 'Kathmandu'),
        (1, 'Lalitpur'),
        (1, 'Bhaktapur'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=250, blank=False)
    l_name = models.CharField(max_length=250, blank=False)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    country = models.PositiveSmallIntegerField(choices=Countries)
    street_add = models.CharField(max_length=250, blank=False)
    apartment = models.CharField(max_length=250, blank=True, null=True)
    town = models.CharField(max_length=250, blank=False)
    state = models.PositiveSmallIntegerField(choices=State)
    postcode = models.CharField(max_length=250, blank=True, null=True)
    phone = models.IntegerField(blank=False)
    email = models.EmailField(max_length=250, blank=False)
    information = models.CharField(max_length=500, blank=True, null=True)



