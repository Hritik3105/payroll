from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import datetime
from payrollapp.models import *
from django.db.models import Q
import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum

def calculate():
    lst=[]
    today = datetime.date.today()
    year = today.year
    val1=year-2
    val4=year+2
    for i in range(int(val1),int(val4)+1):
        lst.append(i)
    
    return lst


@login_required 
def payroll(request):
    ajax_data=request.GET.get("id")
    ajax_data1=request.GET.get("year")
    print("----------------",ajax_data1,ajax_data)

    if request.method =="POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        download=request.POST.get("download")
        view=request.POST.get("view")
        amount=request.POST.get("amount")
       
        total1=""
        if year == "":
            year=0
        week1=""
        week2=""
        week3=""
        week4=""
        if download == "1":
            week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75))
        elif download == "2":
            week2=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75))
        elif download == "3":
            week3=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75))
        elif download == "4":
            week4=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75))
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="paid by month and week.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['VAT ID','Business name', 'Account number',"Amount to pay","Bank code",'Email',"invoice" ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        if download == "1":
            week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75)).values_list('provider_name', 'business_name', 'account', 'amount_paid','bank_code','email','invoice')
            for row in week1:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response
        elif download == "2":
            week2=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75)).values_list('provider_name', 'business_name', 'account', 'amount_paid','bank_code','email','invoice')
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response
        elif download == "3":
    
            week3=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75)).values_list('provider_name', 'business_name', 'account', 'balance_payable','bank_code','email','invoice')
            for row in week3:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response

        elif download == "4":
            

            
            week4=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75)).values_list('provider_name', 'business_name', 'account', 'balance_payable','bank_code','email','invoice')
            for row in week4:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response


        if view == "view1":
            week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75))
           
            return render(request,"Payroll/view.html",{"week":week1})

        if view == "view2":
            week2=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75))
           
            return render(request,"Payroll/view.html",{"week":week2})

        if view == "view3":
            week3=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75))
           
            return render(request,"Payroll/view.html",{"week":week3})

        if view == "view4":
            week4=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75) | Q(week__gt=7.75))
            print(week4)
            return render(request,"Payroll/view.html",{"week":week4})


     
        print("week1",week1)
        print("week2",week2)
        print("week3",week3)
        print("week4",week4)

        cal=calculate()


        return render(request,"Payroll/payroll.html",{"month":month,"year":int(year),"lst":cal})
    cal=calculate()
    print(cal)
    
    total1=0
    total1=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75)).aggregate(Sum('amount_paid'))
    total2=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=1.75,week__lte=3.75)).aggregate(Sum('amount_paid'))
    total3=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=3.75,week__lte=5.75)).aggregate(Sum('amount_paid'))
    total4=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=5.75,week__lte=7.75 )|Q(week__gt=7.75)).aggregate(Sum('amount_paid'))
    print("----------------------===============",total1)
    return render(request,"Payroll/payroll.html",{'lst':cal,'month':ajax_data,"year":ajax_data1,"total1":total1,"total2":total2,"total3":total3,"total4":total4})



def update_date(request,id):

    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        print(month,year)
        print("----------------------",id)
        up_date=Providers.objects.filter(id =id)
        print(up_date)
        cal=calculate()
        return redirect("payroll")
    cal=calculate()
    return render(request,'Payroll/update.html',{"lst":cal})





