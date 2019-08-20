from django.urls import path, re_path
from search import views


app_name = 'search'


urlpatterns = [

    re_path(r'^.*/', views.searchResult, name='searchResult'),

]