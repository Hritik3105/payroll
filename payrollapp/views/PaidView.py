from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Count
from django.db.models import Q




@login_required 
def paid(request):
    lst=[]
    paid_dict={}
    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        print(month,year)

        edit_pro=Providers.objects.filter(Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("business_name",flat=True).distinct()
        for i in edit_pro:
            paid_dict[i] = Providers.objects.filter(Q(business_name=i),Q(month_of_payment=month) & Q(year_of_payment=year)).values_list("invoice",flat=True)
        for i in range(2000,2075):
             lst.append(str(i))
        return render(request,"paid/paid.html",{"obj":paid_dict,"lst":lst,"month":month,"year":year})
    obj_pro=Providers.objects.filter(user_id=request.user.id).values_list("business_name",flat=True).distinct()
    for i in obj_pro:
       
        paid_dict[i] = Providers.objects.filter(business_name=i).values_list("invoice",flat=True)
     
    for i in range(2000,2075):
        lst.append(str(i))
        
    return render(request,"paid/paid.html",{"obj":paid_dict,"lst":lst})



