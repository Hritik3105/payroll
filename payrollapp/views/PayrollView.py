from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def payroll(request):
    lst=[]
    for i in range(2000,2075):
        lst.append(i)
    return render(request,"Payroll/payroll.html",{'lst':lst})