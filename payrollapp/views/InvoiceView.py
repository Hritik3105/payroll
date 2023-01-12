from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.db.models import Q



@login_required 
def invoice(request):
    if request.method == "POST":
        sel_month = request.POST.get("fav_language")
        print("--------------------",sel_month)
        week1_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__lte=30))
        week2_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=30,days_overdue__lte=60))
        week3_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=60,days_overdue__lte=90))
        week4_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=90,days_overdue__lte=120))
        week5_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=120,days_overdue__lte=151))
        week6_pro=Providers.objects.filter(Q(user_id=request.user.id) & Q(days_overdue__gt=151))
        return render(request,"Invoice/invoice.html",{"month":sel_month,'week1_obj':week1_pro,'week2_obj':week2_pro,'week3_obj':week3_pro,'week4_obj':week4_pro,'week5_obj':week5_pro,'week6_obj':week6_pro})

    obj_pro=Providers.objects.filter(user_id=request.user.id)
    return render(request,"Invoice/invoice.html",{'obj':obj_pro})


