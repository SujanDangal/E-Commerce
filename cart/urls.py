from django.urls import path, re_path
from django.conf.urls import url
from .views import *
from . import views
from acereadymade_app import views


app_name = 'cart'

urlpatterns = [
    # Account Parts
    path('detail/', DetailView.as_view(), name='detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('ProceedCheckout/', ProceedCheckoutView.as_view(), name='proceedcheckout'),
    path('ViewCart/', ViewCartView.as_view(), name='viewcart'),
    path('OrderSummery/', OrderView.as_view(), name='order_list'),

    path('add/<int:product_id>/', add_cart, name='add_cart'),
    path('', cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('full_remove/<int:product_id>/', full_remove, name='full_remove'),
# addtocart_2
]