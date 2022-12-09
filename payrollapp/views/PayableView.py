from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def payable(request):
    return render(request,"Payable/payable.html")