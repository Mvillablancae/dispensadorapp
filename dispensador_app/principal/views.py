from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Device

device_list = [
    {
        'owner':'test',
        'ip_addr':'192.168.0.25',
    },
    {
        'owner': 'admin',
        'ip_addr':'192.168.0.26',
    },
    {
        'owner': 'test',
        'ip_addr':'192.168.0.27',
    },
    {
        'owner': 'random_user',
        'ip_addr':'192.168.0.28',
    },
    {
        'owner': 'random_user',
        'ip_addr':'192.168.0.29',
    },
]
@login_required
def home(request):
    context = {
        'devices': Device.objects.all()
    }
    return render(request, 'principal/home.html', context)

@login_required
def devices(request):
    context = {
        'devices':device_list
    }
    return render(request, 'principal/devices.html', context)

@login_required  
def scheduler(request):
    return render(request,'principal/scheduler.html')
