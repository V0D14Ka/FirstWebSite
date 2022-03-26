from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('sendmail', views.sendmail, name='sendmail'),
    path('sent', views.sent, name = 'sent')
]
