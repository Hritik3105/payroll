from .manager import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _



# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    username  = models.CharField(max_length=255,default="")
    email 		= models.EmailField(_('email'),unique=True)
    password    = models.CharField(max_length=255,default="")
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)
    

    USERNAME_FIELD 	='email'
    objects 		= CustomUserManager()
    
    def __str__(self):
        return self.email


class Providers(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  provider_name=models.CharField(max_length=250,null=True,blank=True)
  invoice=models.CharField(max_length=355,null=True,blank=True)
  issue_date=models.DateField(blank=True,null=True)
  total_amount_paid=models.CharField(max_length=250,null=True,blank=True)
  amount_paid=models.CharField(max_length=250,null=True,blank=True)
  balance_payable=models.CharField(max_length=250,null=True,blank=True)
  payment_policy=models.CharField(max_length=250,null=True,blank=True)
  expiration_date=models.DateField(blank=True,null=True)
  payment_week=models.CharField(max_length=250,null=True,blank=True)
  month_of_payment=models.CharField(max_length=250,null=True,blank=True)
  year_of_payment=models.CharField(max_length=250,null=True,blank=True)
  range_to_pay=models.CharField(max_length=250,null=True,blank=True)
  days_overdue=models.CharField(max_length=250,null=True,blank=True)
  overdue=models.CharField(max_length=250,null=True,blank=True)
  business_name=models.CharField(max_length=250,null=True,blank=True)
  month=models.CharField(max_length=250,null=True,blank=True)
  year=models.CharField(max_length=250,blank=True,null=True)
  out_of_time=models.CharField(max_length=250,null=True,blank=True)
