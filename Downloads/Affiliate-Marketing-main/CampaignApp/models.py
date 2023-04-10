from django.db import models
from AdminApp.models import *


# Create your models here.
class Campaign(models.Model):
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  campaign_name=models.CharField(max_length=255,default="")
  influencer_visit=models.CharField(max_length=255,null=True)
  offer=models.CharField(max_length=255,null=True)
  product_discount=models.CharField(max_length=255,null=True)
  product=models.CharField(max_length=255,default="")
  influencer_name=models.CharField(max_length=255,default="")
  coupon=models.CharField(max_length=255,default="")
  date=models.DateField(null=True)
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at =  models.DateTimeField(auto_now=True)
  status=models.IntegerField(default=0)
  description=models.TextField(default="")
  campaign_status= models.IntegerField(default=0) 



class RequestSent(models.Model):
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
  campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True)
  influencee=models.CharField(max_length=200,null=True)
  status=models.BooleanField(default=0)

  
  
class Productdetails(models.Model):
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  product_id=models.CharField(max_length=255,default="")
  
  