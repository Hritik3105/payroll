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
    siiusername = models.CharField(max_length=255,default="",blank=True,null=True)
    siipassword = models.CharField(max_length=255,default="",blank=True,null=True)
    month=models.CharField(max_length=250,null=True,blank=True)
    year=models.CharField(max_length=250,null=True,blank=True)
    

    USERNAME_FIELD 	='email'
    objects 		= CustomUserManager()
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Providers(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  provider_name=models.CharField(max_length=250,null=True,blank=True)
  invoice=models.CharField(max_length=355,null=True,blank=True)
  issue_date=models.DateField(blank=True,null=True)
  total_amount_paid=models.CharField(max_length=250,null=True,blank=True)
  amount_paid=models.IntegerField(null=True,blank=True)
  balance_payable=models.CharField(max_length=250,null=True,blank=True)
  payment_policy=models.CharField(max_length=250,null=True,blank=True)
  expiration_date=models.DateField(blank=True,null=True)
  payment_week=models.CharField(max_length=250,null=True,blank=True)
  month_of_payment=models.CharField(max_length=250,null=True,blank=True)
  year_of_payment=models.CharField(max_length=250,null=True,blank=True)
  range_to_pay=models.CharField(max_length=250,null=True,blank=True)
  days_overdue=models.IntegerField(null=True,blank=True)
  overdue=models.CharField(max_length=250,null=True,blank=True)
  business_name=models.CharField(max_length=250,null=True,blank=True)
  month=models.CharField(max_length=250,null=True,blank=True)
  year=models.CharField(max_length=250,blank=True,null=True)
  out_of_time=models.CharField(max_length=250,null=True,blank=True)
  bank_name=models.CharField(max_length=250,null=True,blank=True)
  bank_code=models.CharField(max_length=250,null=True,blank=True)
  account=models.CharField(max_length=250,null=True,blank=True)
  payment_term=models.CharField(max_length=250,null=True,blank=True)
  email=models.EmailField(null=True,blank=True)
  manual_data=models.FileField(null=True,blank=True)
  week=models.FloatField(blank=True,null=True)
  add1=models.IntegerField(null=True,blank=True)
  add2=models.IntegerField(null=True,blank=True)
  add3=models.IntegerField(null=True,blank=True)
  add4=models.IntegerField(null=True,blank=True)
  add5=models.IntegerField(null=True,blank=True)
  status=models.BooleanField(default=False)
  week1=models.BooleanField(default=False)
  week2=models.BooleanField(default=False)
  week3=models.BooleanField(default=False)
  week4=models.BooleanField(default=False)
  insert_status=models.BooleanField(default=False)
  csv=models.CharField(blank=True,null=True,max_length=255)
  created_at = models.DateField(auto_now_add=True,null=True)
  updated_at =  models.DateField(null=True)
  is_closed=models.BooleanField(default=False)




class Bank(models.Model):
  bank_name=models.CharField(max_length=250,null=True,blank=True)
  bank_code=models.CharField(max_length=250,null=True,blank=True)


class Amountpaid(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  provider=models.ForeignKey(Providers, on_delete=models.CASCADE,null=True)
  amount_paid=models.IntegerField(null=True,blank=True)
  status=models.BooleanField(default=False)

class SII_Month(models.Model):
  month=models.CharField(max_length=200,blank=True,null=True)
  status=models.BooleanField(default=False)
