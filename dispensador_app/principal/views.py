from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Device
from django.contrib.auth.models import User

@login_required
def home(request):
    context = {
        'devices': Device.objects.all(),
        'user': request.user
    }
    return render(request, 'principal/home.html', context)

@login_required
def devices(request):
    context = {
        'devices': Device.objects.all()
    }
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('ip'):
            device=Device()
            device.owner=request.user
            device.ip_addr=request.POST.get('ip')
            device.device_name=request.POST.get('name')
            device.save()
    
    return render(request, 'principal/devices.html', context)

@login_required  
def scheduler(request):
    context = {
        'devices': Device.objects.all()
    }
    return render(request,'principal/scheduler.html', context)

