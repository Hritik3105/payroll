from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def invoice(request):
    return render(request,"Invoice/invoice.html")