from django.urls import path
from . import views
# from django.views.defaults import server_error, page_not_found, permission_denied#


urlpatterns = [
    path('', views.index, name='homepage'),
    path('sendmail', views.sendmail, name='sendmail'),
    path('egg', views.egg, name='egg'),
    path('weather', views.weather, name='weather')
]
