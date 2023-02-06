from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Q


# Show invoice and filter according to days
@login_required 
def invoice(request):

    if request.method == "POST":
        sel_month = request.POST.get("fav_language")
        week1_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__lte=30))
        week2_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=30,days_overdue__lte=60))
        week3_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=60,days_overdue__lte=90))
        week4_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=90,days_overdue__lte=120))
        week5_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=120,days_overdue__lte=150))
        week6_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gte=151))

        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__lte=30)).values_list("amount_paid",flat=True)
        week1_amount=0
        if week1_total:
        
            for i in week1_total:
                print("-----------",type(i))
                if i:
                    week1_amount+=i
        print("week1",week1_amount)


        week2_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=30,days_overdue__lte=60)).values_list("amount_paid",flat=True)
        week2_amount=0
        if week2_total:
            for i in week2_total:
                if i:
                    week2_amount +=i
        print("week2",week2_amount)

        week3_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=60,days_overdue__lte=90)).values_list("amount_paid",flat=True)
        week3_amount=0
        if week3_total:
            for i in week3_total:
                if i:
                    week3_amount +=i
        print("week3",week3_amount)


        week4_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=90,days_overdue__lte=120)).values_list("amount_paid",flat=True)
        week4_amount=0
        if week4_total:
            for i in week4_total:
                if i:
                    week4_amount +=i
        print("week4",week4_amount)


        week5_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=120,days_overdue__lte=150)).values_list("amount_paid",flat=True)

        week5_amount=0
        if week5_total:
            for i in week5_total:
                if i:
                    week5_amount +=i
        print("week5",week5_amount)


        week6_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gte=151)).values_list("amount_paid",flat=True)
        week6_amount=0
        if week6_total:
            for i in week6_total:
                if i:
                    week6_amount +=i
        print("week6",week6_amount)
        return render(request,"Invoice/invoice.html",{"month":sel_month,'week1_obj':week1_pro,'week2_obj':week2_pro,'week3_obj':week3_pro,'week4_obj':week4_pro,'week5_obj':week5_pro,'week6_obj':week6_pro,"week1":week1_amount,"week2":week2_amount,"week3":week3_amount,"week4":week4_amount,"week5":week5_amount,"week6":week6_amount})
  
  
    week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__lte=30)).values_list("amount_paid",flat=True)
    week1_amount=0
    if week1_total:
     
        for i in week1_total:
            print("-----------",type(i))
            if i:
                week1_amount+=i



    week2_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=30,days_overdue__lte=60)).values_list("amount_paid",flat=True)
    week2_amount=0
    if week2_total:
        for i in week2_total:
            if i:
                week2_amount +=i
    print("week2",week2_amount)

    week3_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=60,days_overdue__lte=90)).values_list("amount_paid",flat=True)
    week3_amount=0
    if week3_total:
        
        for i in week3_total:
            print("iiii",i)
            if i:
                week3_amount +=i
    print("week3",week3_amount)


    week4_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=90,days_overdue__lte=120)).values_list("amount_paid",flat=True)
    week4_amount=0
    if week4_total:
        for i in week4_total:
            if i:
                week4_amount +=i
    print("week4",week4_amount)


    week5_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=120,days_overdue__lte=150)).values_list("amount_paid",flat=True)
    week5_amount=0
    if week5_total:
        for i in week5_total:
            if i:
                week5_amount +=i
    print("week5",week5_amount)


    week6_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gte=151)).values_list("amount_paid",flat=True)
    week6_amount=0
    if week6_total:
        for i in week6_total:
            if i:
                week6_amount +=i
    print("week6",week6_amount) 

    obj_pro=Providers.objects.filter(user_id=request.user.id)
    return render(request,"Invoice/invoice.html",{'obj':obj_pro,"week1":week1_amount,"week2":week2_amount,"week3":week3_amount,"week4":week4_amount,"week5":week5_amount,"week6":week6_amount})


