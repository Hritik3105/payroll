from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
import pandas as pd
from django.http import HttpResponse
from django.http import HttpRequest




# def calculate():
   
#     lst=[]
#     obj_pro=Providers.objects.all()
   
#     for i in obj_pro:
#         print("-------------------------",type(i.days_overdue))
#     data = {
#         'customer' : obj_pro,
       
#     }

#     return obj_pro

@login_required 
def invoice(request):

    obj_pro=Providers.objects.filter(user_id=request.user.id)
    return render(request,"Invoice/invoice.html",{'obj':obj_pro})