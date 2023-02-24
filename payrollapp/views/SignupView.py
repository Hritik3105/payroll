from payrollapp.models import *
from django.shortcuts import render,redirect
from django.contrib import messages
from payrollapp.forms.Loginform import *
from payrollapp.forms.Signupform import *
from django.contrib.auth.decorators import login_required
import os


#function to show home page
@login_required 
def home(request):
    z=os.path.exists("/home/ubuntu/payroll/payrollapp/"+request.user.username)
    # z=os.path.exists("/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username)
 
    if z == True:
        return render(request,"home/index.html") 

    else:
        
        directory = request.user.username
        parent_dir = "/home/ubuntu/payroll/payrollapp/"
        # parent_dir = "/home/nirmla/Desktop/payroll/payrollapp"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        return render(request,"home/index.html")
    



#Fucntion for Signup user
def user_signup(request):
    if request.method=="POST":
        form=AddCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(
                    form.cleaned_data.get('password')
                )
            if form.save():
                # messages.success(request,'Account Added Successfully.')
                return redirect('/login')
        else:
            return render(request,"user/signup.html",{'form':form})

    form = AddCreateForm()
    return render(request,"user/signup.html",{'form':form})


    