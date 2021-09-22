from django.urls import path
from . import views, auth
from wall import urls


urlpatterns = [
    path('', views.index), 
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('dashboard/', auth.dashboard),
    path('logout/', auth.logout)
]
