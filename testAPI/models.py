from django.db import models

# Create your models here.
class testUser(models.Model):
    name = models.CharField(max_length=80,unique=True)
    age = models.IntegerField()