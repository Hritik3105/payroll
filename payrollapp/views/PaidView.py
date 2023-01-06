from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *


@login_required 
def paid(request):
    obj_pro=Providers.objects.filter(user_id=request.user.id)
   
    return render(request,"paid/paid.html",{"obj":obj_pro})




#from where we will know balance is paid or not ??