from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Q
import datetime






@login_required 
def paid(request):
    lst=[]
    paid_dict={}
    paid_dict1={}
    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        print(month,year)

        edit_pro=Providers.objects.filter(Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("business_name",flat=True).distinct()
        week=Providers.objects.filter(Q(month_of_payment=month) & Q(year_of_payment=year)).values_list("expiration_date",flat=True)
        count=0
        for i in edit_pro:
            count+=1
            paid_dict[i] = Providers.objects.filter(Q(business_name=i),Q(month_of_payment=month) & Q(year_of_payment=year)).values_list("invoice","week","amount_paid")
        
        for i in range(2000,2075):
             lst.append(str(i))

        return render(request,"paid/paid.html",{"obj":paid_dict,"lst":lst,"month":month,"year":year,"paid":paid_dict1}) 
    today = datetime.date.today()

    year = today.year
    val1=year-2
    val2=year-1
    val3=year+1
    val4=year+2
    for i in range(int(val1),int(val4)+1):
        lst.append(i)
 
        
    return render(request,"paid/filter.html",{"lst":lst})



