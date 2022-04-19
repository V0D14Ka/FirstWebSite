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
    path('profile/<slug:username>', views.profile, name='profile'),
    path('mypage/adduserpost/', views.adduserpost, name='adduserpost'),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept friend request'),
    path('myfriends/', views.myfriends, name='friends'),
    path('changeprofile/', views.changeprofile, name='changeprofile')

]
