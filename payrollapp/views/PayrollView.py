from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import datetime
from payrollapp.models import *
from django.db.models import Q
import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect


def calculate():
    lst=[]
    lst2=[]
    today = datetime.date.today()
    year = today.year
    val1=year-2
    val4=year+2
    for i in range(int(val1),int(val4)+1):
        lst.append(i)
    for i in range(1,5):
        lst2.append(i)
    return lst,lst2



@login_required 
def get_value(request):
    ajax_data=request.GET.get("id")
    ajax_data1=request.GET.get("year")
    print("get_funtion",ajax_data1,ajax_data)
    if request.method =="POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        download=request.POST.get("download")
        view=request.POST.get("view")

        print("get_function",month)
    return ajax_data


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
        request.session['month'] = month
        request.session['year'] = year
        request.session['view'] = view

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


     
        if view:
            print("enterrrrrr1")
            week1=request.POST.get("next")
            return HttpResponseRedirect(week1)


       
        print("week1",week1)
        print("week2",week2)
        print("week3",week3)
        print("week4",week4)

        cal=calculate() 


        return render(request,"Payroll/payroll.html",{"month":month,"year":int(year),"lst":cal})
    cal=calculate()
    month=""
    year=0
 
    total1=0
    total1=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75)).aggregate(Sum('amount_paid'))
    total2=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=1.75,week__lte=3.75)).aggregate(Sum('amount_paid'))
    total3=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=3.75,week__lte=5.75)).aggregate(Sum('amount_paid'))
    total4=Providers.objects.filter(Q(user_id=request.user.id)   & Q(week__gt=5.75,week__lte=7.75 )|Q(week__gt=7.75)).aggregate(Sum('amount_paid'))
    print("----------------------===============",total1)
    if month =="":
        
        month =""
    else:
  
        month = request.session['month']
        
    if  year == 0:
        year = 0
        
    else:
        year = request.session['year']

    
    return render(request,"Payroll/payroll.html",{'lst':cal[0],'month':ajax_data,"year":ajax_data1,"total1":total1,"total2":total2,"total3":total3,"total4":total4,'lst1':cal[1],"month":month,"year":int(year)})



def update_date(request,id):

    if request.method == "POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
        week=request.POST.get("week")
        week1=request.POST.get("next")
        print("----------------------",id)
        up_date=Providers.objects.filter(id=id).update(month_of_payment=month,year_of_payment=year)
        print(up_date)
        cal=calculate()
        return HttpResponseRedirect(week1)
    cal=calculate()
    return render(request,'Payroll/update.html',{"lst":cal[0],'lst1':cal[1]})



def func2(request):
 
    month = request.session['month']
    view= request.session["view"]
    year = request.session['year']
    print("vall",month,view,year)

    
    if view == "view1":
        print("eter view")
        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75))

        if request.method == "POST":
            print("eeeee")
            for i in  range(len(week1)):
                print("value of i",i+1)
                account_id=request.POST.get('id_'+str(i+1))
                account=request.POST.get(str(i+1))
                print("value account",account_id,account)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=account_id)).update(amount_paid=account)
      
            return redirect("payroll")
        return render(request,"Payroll/view.html",{"week":week1})
    
        
     

    if view == "view2":
        week2=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75))
        if request.method == "POST":
            for i in  range(len(week2)):
                print("value of i",i+1)
                account_id=request.POST.get('id_'+str(i+1))
                account=request.POST.get(str(i+1))
                print("value account",account_id,account)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=account_id)).update(amount_paid=account)
            
            return redirect("payroll")
        return render(request,"Payroll/view.html",{"week":week2})

    if view == "view3":
        week3=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75))
        if request.method == "POST":
            for i in  range(len(week3)):
                print("value of i",i+1)
                account_id=request.POST.get('id_'+str(i+1))
                account=request.POST.get(str(i+1))
                print("value account",account_id,account)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=account_id)).update(amount_paid=account)
                
            return redirect("payroll")
        return render(request,"Payroll/view.html",{"week":week3})

    if view == "view4":
        print("Entet4")
        week4=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75) | Q(week__gt=7.75))
        if request.method == "POST":
            print(len(week4))
            for i in  range(len(week4)):
                print("value of i",i+1)
                account_id=request.POST.get('id_'+str(i+1))
                account=request.POST.get(str(i+1))
                print("value account",account_id,account)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=account_id)).update(amount_paid=account)
                print("updated")

            return redirect("payroll")
        return render(request,'Payroll/view.html',{"week":week4})

    return redirect("payroll")