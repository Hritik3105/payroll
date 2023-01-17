from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.http import JsonResponse
from django.core.mail import send_mail as sm
import pandas as pd
import datetime
from django.db.models import F


@login_required 
def index(request):
   
    bank_obj=Bank.objects.all()            
    pro_obj=Providers.objects.filter(user_id=request.user.id).distinct().values("provider_name","business_name")
    lst=[]
    for i in pro_obj:
            
        get=Providers.objects.filter(provider_name=i["provider_name"],user_id=request.user.id).first()
        lst.append(get)     
    print(lst)
       
    z=len(pro_obj)
    return render(request,"provider/index.html",{"bank":bank_obj,"pro":lst,"js":z})


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
    company = request.GET.get("company")
    

    if days == None :
        days=payment_term


    # res = sm(
    #     subject = 'Payroll',
    #     message = 'You are Successfully Register as Provider',
    #     from_email = 'testsood981@gmail.com',
    #     recipient_list = [email],
    #     fail_silently=False,
    # )
  
    val=Providers.objects.filter(user_id=request.user.id) and Providers.objects.filter(business_name=company)
  
    for i in val:
      
        date=pd.to_datetime(i.issue_date).date()
        exp=date+pd.Timedelta(days=int(days))
        months=pd.to_datetime(exp).month_name()
        years=exp.strftime('%Y')


        date_format1 = "%Y-%m-%d"
        
        date1 = datetime.datetime.strptime(str(date), date_format1)
        exp2 = datetime.datetime.strptime(str(exp), date_format1)
        week2=exp2 - date1
      
        weeks=week2.days/4


        exp_week=exp.day/4
        
        date_format = "%Y-%m-%d"
        a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
        # k = datetime.datetime.strptime(str(date, date_format))
        b = datetime.datetime.strptime(str(exp), date_format)
        today= a-b
        print("today",today.days)

        if days:
         
            pro = Providers.objects.filter(business_name = company,id=i.id).update(bank_name=bank_n,account=account_no,payment_term=days,email=email,expiration_date=exp, days_overdue=today.days,week=weeks,month_of_payment=months,year_of_payment=years,bank_code=vat_id) 
            print("pro",pro)
        else:
            pro = Providers.objects.filter(business_name = company,id=i.id).update(bank_name=bank_n,bank_code=vat_id,account=account_no,payment_term=payment_term,email=email,days_overdue=today.days,expiration_date=date,week=weeks,month_of_payment=months,year_of_payment=years) 
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