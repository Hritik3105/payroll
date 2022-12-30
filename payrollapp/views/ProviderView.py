from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
from django.http import JsonResponse

@login_required 
def index(request):
    bank_obj=Bank.objects.all()
    pro_obj=Providers.objects.filter(user_id=request.user.id)
    z=len(pro_obj)
    return render(request,"provider/index.html",{"bank":bank_obj,"pro":pro_obj,"js":z})


@login_required 
def vall(request):
    app=request.GET.get("id")

    
    match= Bank.objects.filter(id=app).values_list("bank_code",flat=True)
    if match:
        apps=match[0]
    
    
    data = {
    "status":"OK",
    "id":apps,
    }

    return JsonResponse(data)