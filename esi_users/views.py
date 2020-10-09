from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# Create your views here.


def register_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'esi_users/register.html', {'form': form})
#https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m


#def index(request):
#    return "index"


def login_view(request):
    return render(request, 'esi_users/login.html')
# https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m