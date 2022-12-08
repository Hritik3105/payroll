from django.contrib.auth import authenticate, login
from payrollapp.models import *
from django.shortcuts import render,redirect
from django.contrib import messages
from payrollapp.forms.Loginform import *
from django.contrib import auth



def user_login(request):
  print("qwee")  
  if request.method == "POST":
    print("enter")
    form = LoginForm(request.POST)
    if form.is_valid():
      uname = form.cleaned_data.get('email')
      print(uname)
      password = form.cleaned_data.get('password')
      print(password)
      user = authenticate(username=uname, password=password)
      if user is not None:
        login(request, user)
        return redirect("home")
      else:
        messages.error(request,"Invalid username or password.")
    else:
      return render(request,"user/login.html",{'form':form})
  form = LoginForm()
  return render(request, "user/login.html",{"form":form})    


def user_logout(request):
  auth.logout(request)
  return redirect('login')