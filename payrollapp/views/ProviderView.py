from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.http import JsonResponse
from django.core.mail import send_mail as sm
import pandas as pd

@login_required 
def index(request):
    bank_obj=Bank.objects.all()            
    pro_obj=Providers.objects.filter(user_id=request.user.id)
    z=len(pro_obj)
    return render(request,"provider/index.html",{"bank":bank_obj,"pro":pro_obj,"js":z})


@login_required 
def vall(request):
    app=request.GET.get("id")
    print(app)

    
    match= Bank.objects.filter(id=app).values_list("bank_code",flat=True)
    if match:
        apps=match[0]
    
    
    data = {
    "status":"OK",
    "id":apps,
    }

    return JsonResponse(data)


@login_required 
def save_val(request):
    bank_c = request.GET.get("id")
    bank_n = request.GET.get("bank_name")
    vat_id = request.GET.get("bank_code")
    account_no = request.GET.get("bank_no")
    payment_term = request.GET.get("payment")
    days = request.GET.get("dayss")
    email = request.GET.get("email")
    if days == None :
        days=payment_term
    res = sm(
        subject = 'Payroll',
        message = 'You are Successfully Register as Provider',
        from_email = 'testsood981@gmail.com',
        recipient_list = [email],
        fail_silently=False,
    )
   
    val=Providers.objects.filter(user_id=request.user.id) and Providers.objects.filter(id=bank_c)
    for i in val:
        date=pd.to_datetime(i.expiration_date).date()

        exp=date+pd.Timedelta(days=int(days))
        print("date",date,"exp",exp)
    if days:
        pro = Providers.objects.filter(id = bank_c).update(bank_name=bank_n,bank_code=vat_id,account=account_no,payment_term=days,email=email,expiration_date=exp) 
    else:
        pro = Providers.objects.filter(id = bank_c).update(bank_name=bank_n,bank_code=vat_id,account=account_no,payment_term=payment_term,email=email) 
    data = {
        "status":"OK",

    }
    return JsonResponse(data)


@login_required 
def pay(request):
    bank_c = request.GET.get("id")
    print("dgdfh",bank_c) 
    data = {
        "status":"OK",

    }
    return JsonResponse(data)