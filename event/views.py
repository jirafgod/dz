from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from event.models import *
import json


@login_required(login_url='/login')
def index(request):
    events = Event.objects.all()
    paginator = Paginator(events, 3)  # Show 4 contacts per page
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginator = Paginator(events, 6)
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    if request.GET.get('ajax'):
        data = {}
        data['list'] = list()
        for event in events:
            inf = {}
            inf['id'] = event.id
            inf['name'] = event.name
            inf['address'] = event.address
            inf['image'] = event.image.url
            inf['description'] = event.description
            data['list'].append(inf)
        data['max'] = paginator.num_pages
        return HttpResponse(json.dumps(data), content_type="application/json")
    form = EventForm(request.user)
    return render(request, 'index.html', {'events': events, 'width': 100, 'form': form.as_p()})

@login_required(login_url='/login')
def event(request, p):
    ev = Event.objects.filter(id=p)
    users = Event_User.objects.filter(event=ev)
    return render(request, 'event.html', {'events': ev, 'width': 60, 'users': users})

@login_required(login_url='/login')
def add_user_event(request, p):
    event = Event.objects.get(id=p)
    eu = Event_User.objects.create(user=request.user, event=event)
    return HttpResponse(request.user.username)


def add_event(request):
        if not request.user.is_authenticated():
            return redirect('/')
        print(request.user)
        form = EventForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('event', p=obj.id)
        return render(request, 'index.html', {'events': events, 'width': 100, 'form': form.as_p()})

def log(request):
    logout(request)
    return redirect('/')

class reg(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'errors': '', 'form': form.as_p()})

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'register.html', {'errors': '', 'form': form.as_p()})

        u = User(username=form.cleaned_data['login'], email=form.cleaned_data['email'],
                 last_name=form.cleaned_data['last_name'], first_name=form.cleaned_data['first_name'])
        u.set_password(form.cleaned_data['password'])
        u.save()
        return render(request, 'login.html', {'errors': ['Вы зарегестрировались, авторизируйтесь.']})


class auth(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        log = request.POST.get('login', '')
        password = request.POST.get('password', '')
        errors = []

        user = authenticate(username=log, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        errors.append('Логин или пароль неверны')
        return render(request, 'login.html', {'errors': errors, 'login': login})
