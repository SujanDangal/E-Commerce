from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard.as_view(), name='dashboard'),
    path('base/', base.as_view(), name='base'),
    path('categories/', categories.as_view(), name='categories'),
    path('add_category/', add_categories.as_view(), name='cat_add_modal'),
    path('order/', order.as_view(), name='order'),
    path('users/', users.as_view(), name='users'),
    path('products/', products.as_view(), name='products'),
    path('add_products/', add_products.as_view(), name='products_add'),
    path('product/delete/<int:product_id>/', DeleteProduct.as_view(), name='delete_product'),
    path('category/delete/<int:category_id>/', DeleteCategory.as_view(), name='delete_category'),
    path('user/delete/<int:user_id>/', DeleteUser.as_view(), name='delete_user'),
    path('edit_category/<int:category_id>/', EditCategory.as_view(), name='edit_category'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('edit_category/<int:category_id>/', EditCategory.as_view(), name='edit_category'),
]
