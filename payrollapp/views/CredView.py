from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.contrib.auth.hashers import make_password

@login_required 
def credential(request):
    user_obj=User.objects.get(id =request.user.id)
    print("clear",user_obj.username)
    obj_pro=Providers.objects.filter(user_id=request.user.id)
    if request.method == "POST":
       
      siusername=request.POST.get("siiusername")
      username=request.POST.get("username")
      password=request.POST.get("password")  
      
      startdate=request.POST.get("startdate")
      enddate=request.POST.get("enddate")  
      user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,startdate=startdate,enddate=enddate,username=username)
      
      return redirect("cred")
    return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro})