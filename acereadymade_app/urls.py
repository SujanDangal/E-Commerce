from django.urls import path, re_path
from django.conf.urls import url
from .views import *
from acereadymade_app import views


app_name = 'acereadymade_app'

urlpatterns = [
    # Account Parts
    path('', IndexView.as_view(), name='index'),
    path('signup/', CustomerSignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
            name='activate'),

    path('details/', DetailsView.as_view(), name='details'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('base/', BaseView.as_view(), name='base'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('myaccount/', MyAccoutView.as_view(), name='myaccount'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),

    path('products/<int:category_id>/<slug:category_slug>/', ProductList.as_view(), name='product_list_by_category'),
    # category's product list

    path('products/', ProductList.as_view(), name='product_list'),
    path('products/detail/<slug:product_slug>/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    # product detail

]