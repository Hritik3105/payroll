from payrollapp.models import *
from django.shortcuts import render,redirect
from django.contrib import messages
from payrollapp.forms.Loginform import *
from payrollapp.forms.Signupform import *
from django.contrib.auth.decorators import login_required

@login_required 
def home(request):
    return render(request,"home/cvvv.html")


def user_signup(request):
    if request.method=="POST":
        form=AddCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(
                    form.cleaned_data.get('password')
                )
            if form.save():
                messages.success(request,'Account Added Successfully.')
                return redirect('/login')
        else:
            return render(request,"user/signup.html",{'form':form})

    form = AddCreateForm()
    return render(request,"user/signup.html",{'form':form})


    