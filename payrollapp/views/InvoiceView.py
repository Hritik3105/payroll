from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
import pandas as pd



hritk="fg"
@login_required 
def invoice(request):
    hritik="sdg"
    
    obj_pro=Providers.objects.filter(user_id=request.user.id)
    return render(request,"Invoice/invoice.html",{'obj':obj_pro})