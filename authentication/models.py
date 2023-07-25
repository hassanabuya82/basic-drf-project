import datetime
from datetime import timedelta, date
from myauth.models import CustomUser as User
from django.utils import timezone

# from django.contrib.auth.models import User

from django.db import models
import random


# Create your models here.
from django.utils import timezone


def generate_reset(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)



class ResetToken(models.Model):
    user = models.OneToOneField(User, related_name='reset_token', on_delete=models.CASCADE)
    token = models.PositiveIntegerField(default=generate_reset(6))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    @property
    def expiry(self):
        return self.created_at + timedelta(hours=1)

    @property
    def status(self):
        return "expired" if timezone.now() > self.expiry else "active"
       

class ActivateToken(models.Model):
    user = models.OneToOneField(User, related_name='activate_token', on_delete=models.CASCADE)
    token = models.PositiveIntegerField(default=generate_reset(6))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    @property
    def expiry(self):
        return self.created_at + timedelta(hours=1)

    @property
    def status(self):   
        return "expired" if timezone.now() > self.expiry else "active"
