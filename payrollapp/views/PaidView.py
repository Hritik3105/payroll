from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def paid(request):
    
    return render(request,"paid/paid.html")