from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Q
import datetime
from django.db.models import Sum



#function to show invoice according to  Date of paid invoice
@login_required 
def paid(request):
    lst=[]
    paid_dict={}
    lst=[]
  
    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")

        edit_pro=Providers.objects.filter(Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("business_name",flat=True).distinct()
        for i in edit_pro:
            paid_dict[i] = Providers.objects.filter(Q(business_name=i),Q(month_of_payment=month) & Q(year_of_payment=year) & Q(user_id=request.user.id)).values_list("invoice","week","amount_paid","add1","add2","add3","add4","add5").order_by("amount_paid")
          
            val1= Providers.objects.filter(Q(business_name=i) & Q(week__gte=0,week__lte=1.75)  & Q(year_of_payment=year) & Q(user_id=request.user.id ) & Q(month_of_payment=month)).aggregate(Sum('amount_paid'))
            val2= Providers.objects.filter(Q(business_name=i) & Q(week__gt=1.75,week__lte=3.75) & Q(year_of_payment=year) & Q(user_id=request.user.id)& Q(month_of_payment=month)).aggregate(Sum('amount_paid'))
            add3 = Providers.objects.filter(Q(business_name=i) & Q(week__gt=3.75,week__lte=5.75) & Q(year_of_payment=year) & Q(user_id=request.user.id)& Q(month_of_payment=month)).aggregate(Sum('amount_paid'))
            add4 = Providers.objects.filter(Q(business_name=i) & Q(week__gt=5.75,week__lte=7.75) & Q(year_of_payment=year) & Q(user_id=request.user.id)& Q(month_of_payment=month)).aggregate(Sum('amount_paid'))
           
            add5 = Providers.objects.filter(Q(business_name=i) & Q(week__gte=7.75) & Q(year_of_payment=year) & Q(user_id=request.user.id)& Q(month_of_payment=month)).aggregate(Sum('amount_paid'))


            up= Providers.objects.filter(Q(business_name=i) & Q(year_of_payment=year) & Q(user_id=request.user.id)).update(add1=val1['amount_paid__sum'],add2=val2["amount_paid__sum"],add3=add3["amount_paid__sum"],add4=add4["amount_paid__sum"],add5=add5["amount_paid__sum"])
         
        week1_lst=[]
        week2_lst=[]
        week3_lst=[]
        week4_lst=[]
        for k,j in paid_dict.items():
         
            for p in j:
                if p[1] >= 0 and p[1] <= 1.75: 
                    week1_lst.append(int(p[2]))
                  
                if p[1] > 1.75 and p[1] <= 3.75: 
                    week2_lst.append(int(p[2]))
                   
                if p[1] >= 3.75 and p[1] <= 5.75: 
                    week3_lst.append(int(p[2]))
                
                if p[1] >= 5.75 and p[1] <= 7.75  or p[1] > 7.75: 
                   week4_lst.append(int(p[2]))
                
            

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
        lst.append(str(i))
 
        
    return render(request,"paid/filter.html",{"lst":lst})



