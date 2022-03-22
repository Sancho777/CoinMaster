from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.conf import settings
from django.contrib.auth.models import Group, User
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.http import HttpResponse
import datetime
from indicador1 import startup1


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def teste():
    catu = datetime.datetime.now()
    return catu


def home(request):

    context = {}
    context['summertime'] = startup1()

    return render(request, 'home.html', context)


def aboutPage(request):
    return render(request, 'about.html')


def indicatorPage(request):
    return render(request, 'indicador.html')

# Create your views here.

# CRUD USER COSTUMER


def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# LOGIN
def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')
