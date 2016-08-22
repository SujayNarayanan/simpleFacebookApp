"""
Definition of models.
"""
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# Create your models here.

class MyAppUser(AbstractBaseUser):
    user_name = models.CharField(max_length=40)
    user_avatar = models.FileField()
    user_access_token = models.CharField(max_length=255, unique=True, default ='default token')
    is_active = models.BooleanField(default = False)