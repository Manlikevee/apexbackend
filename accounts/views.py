from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from home.views import not_authenticated


# Create your views here.




@not_authenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome to your dashboard. ')
            return redirect('userdashboard')  # Replace 'home' with the name of your desired homepage URL
        else:
            messages.error(request, 'Invalid Account ID or Password. ')

    return render(request, 'login.html')
