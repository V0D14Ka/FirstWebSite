from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from pyowm.commons.exceptions import PyOWMError

from .forms import EmailForm
from .forms import WeatherForm
from django.http import HttpResponse, HttpResponseRedirect
from pyowm import OWM
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('c16d779e903477e532485d9034029c6f', config_dict)
mgr = owm.weather_manager()

def index(request):
    return render(request, 'main/index.html')


def sendmail(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = "vodi4kaweb@mail.ru"
            data = {'email': email}
            try:
                send_mail(subject, message, from_email, [email])
            except BadHeaderError:
                return HttpResponse('Invalid Header found')
            return render(request, 'main/sent.html', context=data)
    return render(request, 'main/sendmail.html', {'form': form})


def sent(request):
    return render(request, 'main/sent.html')


def egg(request):
    return render(request, 'main/egg.html')


def weather(request):
    if request.method == 'GET':
        form = WeatherForm()
    else:
        form = WeatherForm(request.POST)
        if form.is_valid():
            pplace = form.cleaned_data['place']
            try:
                observation = mgr.weather_at_place(pplace)
            except PyOWMError:
                return render(request, 'main/badweather.html')
            w = observation.weather
            temp = w.temperature('celsius')['temp']
            max_temp = w.temperature('celsius')['temp_max']
            min_temp = w.temperature('celsius')['temp_min']
            feel_like = w.temperature('celsius')['feels_like']
            status = w.detailed_status
            wind = w.wind()['speed']
            data = {"place": pplace,
                    "temp": temp,
                    "max_temp": max_temp,
                    "min_temp": min_temp,
                    "feel_like": feel_like,
                    "status": status,
                    "wind": wind}
            return render(request, 'main/goodweather.html', context=data)
    return render(request, 'main/weather.html', {'form': form})
