from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='principal-home'),
    path('devices/', views.devices, name='principal-devices'), 
    path('scheduler/', views.scheduler, name='principal-scheduler'), 
]