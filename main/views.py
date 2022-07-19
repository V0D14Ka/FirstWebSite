from bs4 import BeautifulSoup
import os
import requests
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
# from django.contrib.sites import requests
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .tokens import account_activation_token
from .models import *
from .forms import EmailForm, RegisterUserForm, LoginUserForm, UserPostForm, ChangeUserInfo
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


@login_required
def sendmail(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = os.environ['DEFAULT_FROM_EMAIL']
            data = {'email': email}
            try:
                send_mail(subject, message, from_email, [email])
            except:
                return render(request, 'main/bad.html')
            return render(request, 'main/sendmail/sent.html', context=data)
    return render(request, 'main/sendmail/sendmail.html', {'form': form})


def egg(request):
    return render(request, 'main/egg.html')


@login_required
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
                message = "Неккоректный город!"
                return render(request, 'main/weather/weather.html', {'form': form, 'message': message})
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


@login_required
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

    # def form_valid(self, form):
    #     return reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            from_email = os.environ['DEFAULT_FROM_EMAIL']
            mail_subject = 'Активация вашего аккаунта'
            messsage = render_to_string('main/email/emailconfirm.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            context = {'email': to_email}
            send_mail(mail_subject, messsage, from_email, [to_email])
            # messages.success(request,
            #                  "Отлично! Для регистрации осталось только подтвердить"
            #                  " вашу почту. Мы отправили вам письмо с ссылкой.")
            return render(request, 'main/email/emailcheck.html', context=context)
            # return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'main/auth/register.html', {'form': form})


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


@login_required
def logout_user(request):
    logout(request)
    return redirect('homepage')


@login_required
def myfriends(request):
    allusers = User.objects.all()
    allrequests = FriendRequest.objects.filter(to_user=request.user.id)
    friends = request.user.friends.all()
    myrequests = FriendRequest.objects.filter(from_user=request.user.id)
    allu = []
    for user in allusers:
        flag = True
        for to in myrequests:
            if user == to.to_user:
                flag = False
                break
        for i in allrequests:
            if user == i.from_user:
                flag = False
                break
        if flag:
            allu.append(user)
    current_user = request.user
    data = {'current_user': current_user,
            'userposts': UserPost.objects.filter(user_id=current_user.id),
            'allusers': allusers,
            'allrequests': allrequests,
            'friends': friends,
            'myrequests': myrequests,
            'allu': allu,
            }
    return render(request, 'main/profile/friends.html', context=data)


@login_required
def adduserpost(request):
    current_user = request.user
    # userposts = UserPost.objects.filter(user_id=current_user.id)

    if request.method == 'GET':
        form = UserPostForm()
    else:
        form = UserPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            try:
                UserPost.objects.create(title=title, content=content, user_id=current_user.id)
                return HttpResponseRedirect(reverse('profile', kwargs={'username': current_user}))
            except:
                form.add_error(None, "Ошибка добавления поста")
            data = {'current_user': current_user,
                    'form': form,
                    }
            return render(request, 'main/profile/adduserpost.html', context=data)
    return render(request, 'main/profile/adduserpost.html', {'form': form, 'current_user': current_user})


@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    if not request.user.friends.filter(username=User.objects.get(id=userID)).exists():
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return HttpResponseRedirect(reverse('friends'))
        else:
            return HttpResponse('already sent')
    else:
        return HttpResponse('already friend')


@login_required
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponseRedirect(reverse('friends'))
    else:
        return HttpResponse('friend request not accepted')


@login_required
def profile(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        current_user = request.user
        posts = UserPost.objects.filter(user_id=user.id)
        data = {
            'user': user,
            'posts': posts,
            'current_user': current_user,
            'userposts': UserPost.objects.filter(user_id=user.id),

        }
        return render(request, 'main/profile/profile.html', context=data)
    else:
        raise Http404()


@login_required
def changeprofile(request):
    if request == 'GET':
        user = request.user
        form = ChangeUserInfo()
    else:
        form = ChangeUserInfo(request.POST)
        if form.is_valid():
            alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
            current_user = request.user
            username = form.cleaned_data.get('username')
            if not alphabet.isdisjoint(username.lower()):
                form.add_error('username', "Используйте только латиницу!")
            elif current_user.username == username:
                form.add_error('username', "Вы ввели ваш текущий Username!")
            elif User.objects.filter(username=username).exists():
                form.add_error('username', "Пользователь с таким Username уже существует!")
            else:
                try:
                    User.objects.filter(username=current_user).update(username=username)
                    return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
                except:
                    form.add_error(None, "Ошибка изменения данных")
                    data = {'current_user': request.user,
                            'form': form,
                            }
                    return render(request, 'main/profile/changeprofile.html', context=data)
    return render(request, 'main/profile/changeprofile.html', {'form': form, 'current_user': request.user})
