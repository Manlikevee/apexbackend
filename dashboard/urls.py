from django.urls import path

from .views import *
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('mydashboard', userdashboard, name='userdashboard'),
    path('withdrawal', withdrawal, name='withdrawal'),
    path('transactions', transactions, name='transactions'),
    path('register', register, name='register'),
    path('fullTransactiondetail/<str:id>', completetransaction, name='completetransaction'),
    path('vw', your_view, name='your_view'),
    path('admindashboard', superdashboard, name='superdashboard'),
    path('beneficiary', beneficiary, name='beneficiary'),
    path('supportpage', supportpage, name='supportpage'),
    path('contactusdata', contactpage, name='contactusdata'),
    path('FullSupportdetail/<int:id>', supportdetail, name='supportdetail'),
    path('Fullcontactdetaildetail/<int:id>', contactdetail, name='contactdetail'),
    path('userspage', userspage, name='userspage'),
    path('send_email', send_email, name='send_email'),
    path('trans', trans, name='tt'),



]