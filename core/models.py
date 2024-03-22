from django.db import models
from account.models import User
from django.utils import timezone
# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    blood_group = models.CharField(max_length=5)
    blood_pressure = models.CharField(max_length=10)
    disease = models.JSONField(default=dict)
    city=models.CharField(max_length=50,null=True,blank=True)
    date_updated = models.DateField(auto_now=True)