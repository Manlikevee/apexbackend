from django.urls import path

from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', home, name='home'),
    path('about-pwb-finance', aboutus, name='aboutus'),
    path('logout', logout_view, name='logout_view'),
    path('contact-pwb', contactme, name='contactus'),
    path('privacy', privacy, name='privacy'),
    path('terms', terms, name='terms'),



]