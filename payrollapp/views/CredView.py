from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required 
def credential(request):
    print("fgdhgk")
    if request.method == "POST":
      print("entreytr")
      username=request.POST.get("username")
      password=request.POST.get("password")  
      startdate=request.POST.get("startdate")
      enddate=request.POST.get("enddate")  
      
      return redirect("cred")
    return render(request,"cred/sii.html")