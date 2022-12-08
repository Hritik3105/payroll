from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def due_table(request):
    return render(request,"home/table.html")