from django.urls import path
from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/', login_view, name='login'),
]