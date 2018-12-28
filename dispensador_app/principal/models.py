from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=100) 
