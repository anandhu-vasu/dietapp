from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    gender = models.CharField(max_length=8)
    age = models.IntegerField()
    occupation = models.CharField(max_length=20)
    height = models.FloatField(max_length=25)
    weight = models.FloatField(max_length=25)
    diet_plan = models.CharField(max_length=25)
    veg = models.CharField(max_length=1)
    disease = models.CharField(max_length=25)
    allergy = models.CharField(max_length=25)
    breakfast = models.CharField(max_length=450)
    lunch =  models.CharField(max_length=450)
    dinner = models.CharField(max_length=450)
    date= models.DateTimeField(auto_now_add=True)


class Form(models.Model):
    gender = models.CharField(max_length=8)
    age = models.IntegerField()
    occupation = models.CharField(max_length=20)
    height = models.FloatField(max_length=25)
    weight = models.FloatField(max_length=25)
    diet_plan = models.CharField(max_length=25)
    veg = models.CharField(max_length=1)
    disease = models.CharField(max_length=25)
    allergy = models.CharField(max_length=25)
