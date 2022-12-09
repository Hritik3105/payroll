from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def payroll(request):
    return render(request,"Payroll/payroll.html")