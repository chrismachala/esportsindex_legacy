from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from esi_users.models import Profile, Future
from esi_players.models import Player
import esi_users.forms as forms
from django.contrib.auth.decorators import login_required
import sys
# Create your views here.


def register_view(request):
    form = forms.UserCreateForm(request.POST)
    print('form is valid = {0}'.format(form.is_valid()))
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        print(form.errors)
        form = forms.UserCreateForm()
    return render(request, 'esi_users/register.html', {'form': form})


@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    u = request.user
    f_query = Future.objects.filter(user=u.profile)
    template_name = 'esi_users/home.html'
    return render(request, template_name, {'futures': f_query})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "esi_users/login.html", {"form": form})
