from django.urls import path
from . import views
# from django.views.defaults import server_error, page_not_found, permission_denied#


urlpatterns = [
    path('', views.index, name='homepage'),
    path('sendmail/', views.sendmail, name='sendmail'),
    path('egg/', views.egg, name='egg'),
    path('weather/', views.weather, name='weather'),
    path('horoscope/', views.horoscope, name='horoscope'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('emailVerification/<uidb64>/<token>', views.activate, name='emailActivate'),
    path('mypage/', views.mypage, name='mypage')
]
