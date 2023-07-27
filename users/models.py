from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # image = models.ImageField()
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password','acc_activated']