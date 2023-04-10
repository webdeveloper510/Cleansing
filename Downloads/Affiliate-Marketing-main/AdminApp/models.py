from django.db import models
from AdminApp.manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    CHOICES=(
      ("2","Influencer"),
      ("3","Vendor")
    )
    username  = models.CharField(max_length=255,default="")
    email 		= models.EmailField(_('email'),unique=True)
    password    = models.CharField(max_length=255,default="")
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    user_type = models.CharField(default="",max_length=255,choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)
    country= models.CharField(max_length=255,blank=True,null=True)
    shopify_url=models.CharField(max_length=255,blank=True,null=True,unique=True)
    instagram_url=models.CharField(max_length=255,blank=True,null=True)
    category=models.CharField(max_length=255,blank=True,null=True)
    

    USERNAME_FIELD 	='email'
    
    objects 		= CustomUserManager()
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
