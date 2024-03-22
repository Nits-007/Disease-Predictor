from django.urls import path
from .views import *



app_name = 'users'
urlpatterns = [
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
]