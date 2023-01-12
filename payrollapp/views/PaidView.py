from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Q
import datetime

#Date of paid invoice
@login_required 
def paid(request):
    lst=[]
    paid_dict={}
   
    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")

        edit_pro=Providers.objects.filter(Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("business_name",flat=True).distinct()
        for i in edit_pro:
            paid_dict[i] = Providers.objects.filter(Q(business_name=i),Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("invoice","week","amount_paid").order_by("amount_paid")
        print("------------------",paid_dict)
        
        week1_lst=[]
        week2_lst=[]
        week3_lst=[]
        week4_lst=[]
        for k,j in paid_dict.items():
            for a in j:
                if a[1] >= 0 and a[1] <= 1.75: 
                   
                    week1_lst.append(int(a[2]))
                  
                if a[1] > 1.75 and a[1] <= 3.75: 
                 
                    week2_lst.append(int(a[2]))
                   
                if a[1] >= 3.75 and a[1] <= 5.75: 
                   
                    week3_lst.append(int(a[2]))
                
                if a[1] >= 5.75 and a[1] <= 7.75: 
                   
                    week4_lst.append(int(a[2]))
                
        week1=sum(week1_lst)           
        week2=sum(week2_lst)  
        week3=sum(week3_lst) 
        week4=sum(week4_lst)  
  
        for i in range(2000,2075):
             lst.append(str(i))

        return render(request,"paid/paid.html",{"obj":paid_dict,"lst":lst,"month":month,"year":year,"week1":week1,"week2":week2,"week3":week3,"week4":week4}) 
    today = datetime.date.today()

    year = today.year
    val1=year-2
    val2=year-1
    val3=year+1
    val4=year+2
    for i in range(int(val1),int(val4)+1):
        lst.append(i)
 
        
    return render(request,"paid/filter.html",{"lst":lst})



