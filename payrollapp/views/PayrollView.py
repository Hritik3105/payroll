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
from django.http import JsonResponse
from django.contrib import messages



# function help to get dropdown value
def calculate():
    lst=[]
    lst2=[]
    today = datetime.date.today()
    year = today.year
    val1=year-2
    val4=year+2
    for i in range(int(val1),int(val4)+1):
        lst.append(str(i))
    for i in range(1,5):

        lst2.append(i)
 
    return lst,lst2



# to view payroll amount and go inside the payroll
@login_required 
def payroll(request):
   
    ajax_data=request.GET.get("id")
    ajax_data1=request.GET.get("year")
    if request.method =="POST":
        month=request.POST.get("month")
        year=request.POST.get("year")
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
         
        if view:
           
            week1=request.POST.get("next")
            return HttpResponseRedirect(week1)

        cal=calculate() 
        

        return render(request,"Payroll/payroll.html",{"month":month,"year":int(year),"lst":cal})
    cal=calculate()
    month=""
    year=0
    total1=0
    total1=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75)).aggregate(Sum('amount_paid'))
    # total122=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75)).values_list('amount_paid','month_of_payment','year_of_payment')
    total2=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=1.75,week__lte=3.75)).aggregate(Sum('amount_paid'))
    total3=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=3.75,week__lte=5.75)).aggregate(Sum('amount_paid'))
    total4=Providers.objects.filter(Q(user_id=request.user.id)   & Q(week__gt=5.75,week__lte=7.75 )|Q(week__gt=7.75)).aggregate(Sum('amount_paid'))

    if month =="":
        
        month =""
    else:
  
        month = request.session['month']
        
    if  year == 0:
        year = 0
        
    else:
        year = request.session['year']
    return render(request,"Payroll/payroll.html",{'lst':cal[0],'month':ajax_data,"year":ajax_data1,"total1":total1,"total2":total2,"total3":total3,"total4":total4,'lst1':cal[1],"month":month,"year":int(year)})




#Download excel file for payroll
@login_required 
def func2(request):
   
    arrr=[]
    month = request.session['month']
    view= request.session["view"]
    year = request.session['year']
    

    ajax_data1=request.GET.get("val")
    if view == "view1":
        
        cal=calculate()
        stats1=Providers.objects.filter(user_id=request.user.id).values_list('week1',flat=True)
        stats2=Providers.objects.filter(user_id=request.user.id).values_list('week2',flat=True)
        stats3=Providers.objects.filter(user_id=request.user.id).values_list('week3',flat=True)
        stats4=Providers.objects.filter(user_id=request.user.id).values_list('week4',flat=True)


        if True in stats4:
          
            cal[1].remove(4)

        if True in stats3:
          
            cal[1].remove(3)
        
        if True in stats2:
           
            cal[1].remove(2)
        
        if True in stats1:
            
            cal[1].remove(1)
           
       
        else:
            cal[1]
           
        if request.method == "POST" and "download" in request.POST:
            
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
            
            week12=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=0,week__lte=1.75)).values_list("provider_name","business_name","account","amount_paid","bank_code","email","invoice")
            for row in week12:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            data1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75)).update(status=True,week1=True)
            return response

        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75))
        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75)).aggregate(Sum("amount_paid"))
        week_tl=week1_total["amount_paid__sum"]
        status_upd=Amountpaid.objects.filter(user_id=request.user.id).values_list("status",flat=True)
        status_id=Amountpaid.objects.filter(user_id=request.user.id).values_list("provider",flat=True)
        data=Amountpaid.objects.filter(user_id=request.user.id)
      
        request.session['upt_month']= ""
        request.session['upt_year'] ="" 

   
        if status_upd and status_id:
            status_value=status_upd[0]
            status_ids=status_id
           
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        year2 = request.session['upt_month']
        month2 = request.session['upt_year']
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":1,"week_total":week_tl,'week_status':stats1})

        
     

    if view == "view2":
        cal=calculate()
        stats1=Providers.objects.filter(user_id=request.user.id).values_list('week1',flat=True)
        stats2=Providers.objects.filter(user_id=request.user.id).values_list('week2',flat=True)
        stats3=Providers.objects.filter(user_id=request.user.id).values_list('week3',flat=True)
        stats4=Providers.objects.filter(user_id=request.user.id).values_list('week4',flat=True)


        if True in stats4:
          
            cal[1].remove(4)

        if True in stats3:
          
            cal[1].remove(3)
        
        if True in stats2:
           
            cal[1].remove(2)
        
        if True in stats1:
            
            cal[1].remove(1)
           
       
        else:
            cal[1]
           

        if request.method == "POST" and "download" in request.POST:
            
            
            response = HttpResponse(content_type='application/ms-excel' )
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
           
            
            week122=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75)).values_list("provider_name","business_name","account","amount_paid","bank_code","email","invoice")
            for row in week122:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75)).update(status=True,week2=True)
            return response

        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75))
        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=1.75,week__lte=3.75)).aggregate(Sum("amount_paid"))
        week_tl=week1_total["amount_paid__sum"]
        status_upd=Amountpaid.objects.filter(user_id=request.user.id).values_list("status",flat=True)
        status_id=Amountpaid.objects.filter(user_id=request.user.id).values_list("provider",flat=True)
        data=Amountpaid.objects.filter(user_id=request.user.id)
       
   
        if status_upd and status_id:
            status_value=status_upd[0]
            status_ids=status_id
            print("sfgdhkdkjfhfjkhkjhkkjhkjh",status_ids)
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":2,"week_total":week_tl,'week_status':stats2})



    if view == "view3":
        cal=calculate()
        stats1=Providers.objects.filter(user_id=request.user.id).values_list('week1',flat=True)
        stats2=Providers.objects.filter(user_id=request.user.id).values_list('week2',flat=True)
        stats3=Providers.objects.filter(user_id=request.user.id).values_list('week3',flat=True)
        stats4=Providers.objects.filter(user_id=request.user.id).values_list('week4',flat=True)


        if True in stats4:
          
            cal[1].remove(4)

        if True in stats3:
          
            cal[1].remove(3)
        
        if True in stats2:
           
            cal[1].remove(2)
        
        if True in stats1:
            
            cal[1].remove(1)
           
       
        else:
            cal[1]
           
        
     
        if request.method == "POST" and "download" in request.POST:
            
         
            response = HttpResponse(content_type='application/ms-excel' )
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
          
            week123=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75)).values_list("provider_name","business_name","account","amount_paid","bank_code","email","invoice")
            for row in week123:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            data1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75)).update(status=True,week3=True)
            return response

        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75))
        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=3.75,week__lte=5.75)).aggregate(Sum("amount_paid"))
        week_tl=week1_total["amount_paid__sum"]
        status_upd=Amountpaid.objects.filter(user_id=request.user.id).values_list("status",flat=True)
        status_id=Amountpaid.objects.filter(user_id=request.user.id).values_list("provider",flat=True)
        data=Amountpaid.objects.filter(user_id=request.user.id)
        

   
        if status_upd and status_id:
            status_value=status_upd[0]
            status_ids=status_id
            
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":3,"week_total":week_tl,'week_status':stats3})


    if view == "view4":
        cal=calculate()
        stats1=Providers.objects.filter(user_id=request.user.id).values_list('week1',flat=True)
        stats2=Providers.objects.filter(user_id=request.user.id).values_list('week2',flat=True)
        stats3=Providers.objects.filter(user_id=request.user.id).values_list('week3',flat=True)
        stats4=Providers.objects.filter(user_id=request.user.id).values_list('week4',flat=True)


        if True in stats4:
          
            cal[1].remove(4)

        if True in stats3:
          
            cal[1].remove(3)
        
        if True in stats2:
           
            cal[1].remove(2)
        
        if True in stats1:
            
            cal[1].remove(1)

        else:
            cal[1]

        if request.method == "POST" and "download" in request.POST:
            
           
            response = HttpResponse(content_type='application/ms-excel' )
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
           
            week124=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75)).values_list("provider_name","business_name","account","amount_paid","bank_code","email","invoice")
            for row in week124:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            
            wb.save(response)
            data1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75)).update(status=True,week4=True)
            return response

        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75))
        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gt=5.75,week__lte=7.75)).aggregate(Sum("amount_paid"))
        week_tl=week1_total["amount_paid__sum"]
        status_upd=Amountpaid.objects.filter(user_id=request.user.id).values_list("status",flat=True)
        status_id=Amountpaid.objects.filter(user_id=request.user.id).values_list("provider",flat=True)
        data=Amountpaid.objects.filter(user_id=request.user.id)
   
        if status_upd and status_id:
            status_value=status_upd[0]
            status_ids=status_id
            
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":4,"week_total":week_tl,'week_status':stats4})

    return redirect("payroll")



# Get the total amount of payroll
@login_required 
def option_value(request):
    provider_ids=request.GET.get("month")

    provider_id=request.GET.get("ids")
   
    bal_id= request.session["month"]
    bal_year= request.session["year"]
    
    calu_value=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75) & Q(month_of_payment=provider_id) & Q(year_of_payment=provider_id))
    
    data={
        "month":bal_id,
    }

    return JsonResponse(data)



#Get the amount after calculation
@login_required 
def rem_amt(request):
    pay_id=request.GET.get("id").replace(",","")
    pay_amt=request.GET.get("amt").replace(",","")
    print("dfsffffffffff",pay_id)
   
    getval=request.GET.get("actual")
    if getval:
        getval.replace(",","")
    amt_diff=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=pay_id)).values_list("amount_paid",flat=True)
    chng= amt_diff[0]
    print(chng)
    
    final_amt = chng - int(pay_amt)

    data={
        "amount":final_amt,
        "amount2":getval
    }

    return JsonResponse(data)




#Save the data into db after calculation
@login_required 
def save_data(request):
    print("submit button click")
    year=request.GET.get("year")
    month=request.GET.get("month")
    week=request.GET.get("week")
    weekgot=request.GET.get("week")
    id=request.GET.get("id").replace(",","")
    pay_amt=request.GET.get("amt").replace(",","")
    user_id=request.user.id
    if week == "" or week == "Week":
        week=0
    if id == "" :
        id =0
    id_amt=request.GET.get("amt").replace(",","")   
    
    if week == "1":
        week=1
    elif week == "2":
        week=2
    elif week == "3":
        week= 3.90
    elif week == "4":
        week =7

    request.session["upt_month"]=month  
    request.session["upt_year"]=year
    request.session["upt_week"]=week
    amt_diff=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=id)).values_list("amount_paid",flat=True)
    
    chng= amt_diff[0]
   
    final_amt = chng - int(pay_amt)
    
    sav_data=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=id)).update(amount_paid=pay_amt)
    res_data=Providers.objects.filter(id=int(id)).values("business_name","invoice","payment_term")
    if res_data:
        inst_data=Providers.objects.filter(user_id=request.user.id).create(month_of_payment=month,year_of_payment=year,week=week,business_name=res_data[0]["business_name"],invoice=res_data[0]["invoice"],amount_paid=id_amt,user_id=request.user.id,payment_term=res_data[0]["payment_term"])

    data={
        "status":"success",
        "record":final_amt,
        "user":user_id
    }
    messages.success(request, "Your Payrol is Reschedule to  month " + str(month) + " year "  + str(year) + "  and " + " week " + str(weekgot) )
    return JsonResponse(data)



@login_required 
def save_data2(request):
    print("submits button click")
    year=request.GET.get("year")
    month=request.GET.get("month")
    week=request.GET.get("week")
    weekgot=request.GET.get("week")
    
    id=request.GET.get("id").replace(",","")
    pay_amt=request.GET.get("amt").replace(",","")
    user_id=request.user.id
    if week == "" or week == "Week":
        week=0
    if id == "" :
        id =0
    id_amt=request.GET.get("amt").replace(",","")   
    
    if week == "1":
        week=1
    elif week == "2":
        week=2
    elif week == "3":
        week= 3.90
    elif week == "4":
        week =7

    request.session["upt_month"]=month  
    request.session["upt_year"]=year
    request.session["upt_week"]=week
    amt_diff=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=id)).values_list("amount_paid",flat=True)
    
    chng= amt_diff[0]
   
    final_amt = chng - int(pay_amt)
    
    sav_data=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=id)).update(amount_paid=pay_amt)
    res_data=Providers.objects.filter(id=int(id)).values("business_name","invoice","payment_term")
    if res_data:
        inst_data=Providers.objects.filter(user_id=request.user.id).create(month_of_payment=month,year_of_payment=year,week=week,business_name=res_data[0]["business_name"],invoice=res_data[0]["invoice"],amount_paid=id_amt,user_id=request.user.id,payment_term=res_data[0]["payment_term"])

    data={
        "status":"success",
        "record":final_amt,
        "user":user_id
    }
    messages.success(request, "Your Payrol is Reschedule to  month " + str(month) + " year "  + str(year) + "  and " + " week " + str(weekgot) )
    return JsonResponse(data)


#Reschedule payroll
def data_reschedule(request):
    year=request.GET.get("year")
    month=request.GET.get("month")
    week=request.GET.get("week")
    
    if week == "" or week == "Week":
        week=0
   
    id=request.GET.get("id").replace(",","")
    if id == "" :
        id =0
    id_amt=request.GET.get("amt")
    
    if week == "1":
        week=1
    elif week == "2":
        week=2
    elif week == "3":
        week= 3.90
    elif week == "4":
        week =7
    res_data=Providers.objects.filter(id=int(id)).values("business_name","invoice","payment_term")

    if res_data:
        inst_data=Providers.objects.filter(user_id=request.user.id).create(month_of_payment=month,year_of_payment=year,week=week,business_name=res_data[0]["business_name"],invoice=res_data[0]["invoice"],amount_paid=id_amt,user_id=request.user.id,payment_term=res_data[0]["payment_term"])

    data={
        "message":"hello"
    }

    return JsonResponse(data)


@login_required 
def rem_amt1(request):
    pay_id=request.GET.get("month")
    pay_amt=request.GET.get("year")
    print("dfsffffffffff",pay_id,pay_amt)
    total1=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75) & Q(month_of_payment=pay_id)& Q(year_of_payment=pay_amt)).aggregate(Sum('amount_paid'))
    total2=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=1.75,week__lte=3.75) & Q(month_of_payment=pay_id)& Q(year_of_payment=pay_amt)).aggregate(Sum('amount_paid'))
    total3=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=3.75,week__lte=5.75) & Q(month_of_payment=pay_id)& Q(year_of_payment=pay_amt)).aggregate(Sum('amount_paid'))
    total4=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gt=5.75,week__lte=7.75) & Q(month_of_payment=pay_id)& Q(year_of_payment=pay_amt)).aggregate(Sum('amount_paid'))
    data={
        "amount1":total1,
        "amount2":total2,
        "amount3":total3,
        "amount4":total4,
     
    }

    return JsonResponse(data)