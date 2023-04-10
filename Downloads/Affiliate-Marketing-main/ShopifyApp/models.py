from django.db import models
from AdminApp.models import *


# Create your models here.

class Coupon(models.Model):
    vendorid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    coupon=models.CharField(max_length=255,blank=True,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)