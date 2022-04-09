from bs4 import BeautifulSoup
import os
import requests

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.sites import requests
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .tokens import account_activation_token
from .models import *
from .forms import EmailForm, RegisterUserForm, LoginUserForm
from .forms import WeatherForm
from .forms import HoroscopeForm

from pyowm import OWM
from pyowm.commons.exceptions import PyOWMError
from pyowm.utils.config import get_default_config

key_pyowm = os.environ['key_pyowm']

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM(key_pyowm, config_dict)
mgr = owm.weather_manager()


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'main/index.html', context=context)


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
            except:
                return render(request, 'main/bad.html')
            return render(request, 'main/sendmail/sent.html', context=data)
    return render(request, 'main/sendmail/sendmail.html', {'form': form})


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
                return render(request, 'main/bad.html')
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
            return render(request, 'main/weather/goodweather.html', context=data)
    return render(request, 'main/weather/weather.html', {'form': form})


def horoscope(request):
    if request.method == 'GET':
        form = HoroscopeForm()
    else:
        form = HoroscopeForm(request.POST)
        if form.is_valid():
            ssign = form.cleaned_data['sign']
            try:
                res = requests.get(f"https://www.astrostar.ru/horoscopes/main/{ssign}/day.html")
            except:
                return render(request, 'main/bad.html')
            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find("p")
            content = {"scope": data.text,
                       'sign': ssign}
            return render(request, 'main/horoscope/goodscope.html', context=content)
    return render(request, 'main/horoscope/horoscope.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/auth/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активация вашего аккаунта'
            message = render_to_string('main/email/emailconfirm.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            context = {'email': to_email}
            send_mail(mail_subject, message, 'vodi4kaweb@mail.ru', [to_email])
            return render(request, 'main/email/emailcheck.html', context=context)


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'main/email/emailsucceed.html')
    else:
        return render(request, 'main/email/badmail.html')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


def logout_user(request):
    logout(request)
    return redirect('homepage')


