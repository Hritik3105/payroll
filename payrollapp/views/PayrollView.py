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
    print("-=-=-==",lst2)
    print("-=-=-ghj==",lst)
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
            week1=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gte=0,provider__week__lte=1.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week1:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response
        elif download == "2":
            week2=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=1.75,provider__week__lte=3.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response
        elif download == "3":
            week3=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=3.75,provider__week__lte=5.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week3:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)

            return response

        elif download == "4":
            week4=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=5.75,provider__week__lte=7.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
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
        if week == "1":
            week=1
        elif week == "2":
            week=2
        elif week == "3":
            week= 3.90

        elif week == "4":
            week =7

        week1=request.POST.get("next")
        print("----------------------",id)
        up_date=Providers.objects.filter(id=id).update(month_of_payment=month,year_of_payment=year,week=week)
        print(up_date)
        cal=calculate()
        return HttpResponseRedirect(week1)
    cal=calculate()
    return render(request,'Payroll/update.html',{"lst":cal[0],'lst1':cal[1]})



def func2(request):
    arrr=[]
    month = request.session['month']
    view= request.session["view"]
    year = request.session['year']
    print("vall",month,view,year)

    ajax_data1=request.GET.get("val")
    if view == "view1":
        cal=calculate()

        if request.method == "POST"  and "updt" in request.POST:
            pro_obj=Amountpaid()
         
            provider_id=request.POST.get("id")
            provider_account=request.POST.get("amt")
            chn_month = request.POST.get("month")
            chn_year=request.POST.get("year")
            week=request.POST.get("week")
            upd_proid=provider_id.replace(",","")
            upd_product=provider_account.replace(",","")
            pro_obj.user_id=request.user.id
            pro_obj.provider_id=upd_proid
            pro_obj.amount_paid=int(upd_product)
          
            pro_obj.save()
            amt_cal=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).values_list("amount_paid",flat=True)
            if amt_cal:
                final_amt=int(amt_cal[0])-int(upd_product)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).update(amount_paid=final_amt)
            print(chn_month,chn_year,week,upd_proid,upd_product)
            return redirect("payroll")

        if request.method == "POST" and "download" in request.POST:
            
            print("enrtryrty")
            provider_id=request.POST.get("upd")
            print("ddsfsd",provider_id)
            upd_proid=provider_id.replace(",","")
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
            upd_status=Amountpaid.objects.filter(user_id=request.user.id,provider_id=upd_proid).update(status=True)
            
            week2=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=0,provider__week__lte=1.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
          
            return response

        week1=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75))
        week1_total=Providers.objects.filter(Q(user_id=request.user.id) & Q(month_of_payment=month) & Q(year_of_payment=year) & Q(week__gte=0,week__lte=1.75)).aggregate(Sum("amount_paid"))
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
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":1,"week_total":week_tl})

        
     

    if view == "view2":
        cal=calculate()
        if request.method == "POST"  and "updt" in request.POST:
            pro_obj=Amountpaid()
         
            provider_id=request.POST.get("id")
            provider_account=request.POST.get("amt")
            chn_month = request.POST.get("month")
            chn_year=request.POST.get("year")
            week=request.POST.get("week")
            upd_proid=provider_id.replace(",","")
            upd_product=provider_account.replace(",","")
            pro_obj.user_id=request.user.id
            pro_obj.provider_id=upd_proid
            pro_obj.amount_paid=int(upd_product)
          
            pro_obj.save()
            amt_cal=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).values_list("amount_paid",flat=True)
            if amt_cal:
                final_amt=int(amt_cal[0])-int(upd_product)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).update(amount_paid=final_amt)
            print(chn_month,chn_year,week,upd_proid,upd_product)
            return redirect("payroll")

        if request.method == "POST" and "download" in request.POST:
            
            print("enrtryrty")
            provider_id=request.POST.get("upd")
            upd_proid=provider_id.replace(",","")
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
            upd_status=Amountpaid.objects.filter(user_id=request.user.id,provider_id=upd_proid).update(status=True)
            
            week2=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=1.75,provider__week__lte=3.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
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
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":2,"week_total":week_tl})



    if view == "view3":
        cal=calculate()
        if request.method == "POST"  and "updt" in request.POST:
            pro_obj=Amountpaid()
         
            provider_id=request.POST.get("id")
            provider_account=request.POST.get("amt")
            chn_month = request.POST.get("month")
            chn_year=request.POST.get("year")
            week=request.POST.get("week")
            upd_proid=provider_id.replace(",","")
            upd_product=provider_account.replace(",","")
            pro_obj.user_id=request.user.id
            pro_obj.provider_id=upd_proid
            pro_obj.amount_paid=int(upd_product)
          
            pro_obj.save()
            amt_cal=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).values_list("amount_paid",flat=True)
            if amt_cal:
                final_amt=int(amt_cal[0])-int(upd_product)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).update(amount_paid=final_amt)
            print(chn_month,chn_year,week,upd_proid,upd_product)
            return redirect("payroll")

        if request.method == "POST" and "download" in request.POST:
            
            print("enrtryrty")
            provider_id=request.POST.get("upd")
            upd_proid=provider_id.replace(",","")
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
            upd_status=Amountpaid.objects.filter(user_id=request.user.id,provider_id=upd_proid).update(status=True)
            
            week2=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=3.75,provider__week__lte=5.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
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
            print("sfgdhkdkjfhfjkhkjhkkjhkjh",status_ids)
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        return render(request,"Payroll/view.html",{"week":week1,"lst":cal[0],'lst1':cal[1],"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":3,"week_total":week_tl})


    if view == "view4":
        if request.method == "POST"  and "updt" in request.POST:
            pro_obj=Amountpaid()
         
            provider_id=request.POST.get("id")
            provider_account=request.POST.get("amt")
            chn_month = request.POST.get("month")
            chn_year=request.POST.get("year")
            week=request.POST.get("week")
            upd_proid=provider_id.replace(",","")
            upd_product=provider_account.replace(",","")
            pro_obj.user_id=request.user.id
            pro_obj.provider_id=upd_proid
            pro_obj.amount_paid=int(upd_product)
          
            pro_obj.save()
            amt_cal=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).values_list("amount_paid",flat=True)
            if amt_cal:
                final_amt=int(amt_cal[0])-int(upd_product)
                upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).update(amount_paid=final_amt)
            print(chn_month,chn_year,week,upd_proid,upd_product)
            return redirect("payroll")

        if request.method == "POST" and "download" in request.POST:
            
            print("enrtryrty")
            provider_id=request.POST.get("upd")
            upd_proid=provider_id.replace(",","")
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
            upd_status=Amountpaid.objects.filter(user_id=request.user.id,provider_id=upd_proid).update(status=True)
            
            week2=Amountpaid.objects.filter(user_id=request.user.id).select_related("provider").filter(provider__week__gt=5.75,provider__week__lte=7.75).values_list("provider__provider_name","provider__business_name","provider__account","amount_paid","provider__bank_code","provider__email","provider__invoice")
            for row in week2:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
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
            print("sfgdhkdkjfhfjkhkjhkkjhkjh",status_ids)
        else:
            status_value=0
            status_ids=0
        year = request.session['year']
        month = request.session['month']
        return render(request,"Payroll/view.html",{"week":week1,"status":status_value,"status_ids":status_ids,"data":data,"year":year,"month":month,"weeks":4,"week_total":week_tl})


    return redirect("payroll")




def get_value(request):
    if request.method == "POST":
        provider_id=request.POST.get("month")
        return redirect("payroll")

    return redirect("payroll")
    # provider_id=request.GET.get("id")
    # upd_proid=provider_id.replace(",","")
    # provider_account=request.GET.get("balance")
    # upd_product=provider_account.replace(",","")

    # pro_obj=Amountpaid()
    # pro_obj.user_id=request.user.id
    # pro_obj.provider_id=upd_proid
    # pro_obj.amount_paid=int(upd_product)
    # pro_obj.save()
    # amt_cal=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).values_list("amount_paid",flat=True)
    # if amt_cal:
    #     final_amt=int(amt_cal[0])-int(upd_product)
    #     upd=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=upd_proid)).update(amount_paid=final_amt)
    # else:
    #     amt_cal=0
    # data={
    #     "pro":provider_account
    # }
    # return JsonResponse(data)



def option_value(request):
    provider_ids=request.GET.get("month")
    print(provider_ids)
    provider_id=request.GET.get("ids")
   
    print("0-0-0-",provider_id)
   
    bal_id= request.session["month"]
    bal_year= request.session["year"]
    
    calu_value=Providers.objects.filter(Q(user_id=request.user.id) & Q(week__gte=0,week__lte=1.75) & Q(month_of_payment=provider_id) & Q(year_of_payment=provider_id))
    
    data={
        "month":bal_id,
    }

    return JsonResponse(data)



def rem_amt(request):
    pay_id=request.GET.get("id").replace(",","")
    pay_amt=request.GET.get("amt").replace(",","")
    print(pay_id)
    print(pay_amt)
    amt_diff=Providers.objects.filter(Q(user_id=request.user.id) & Q(id=pay_id)).values_list("amount_paid",flat=True)
    chng= amt_diff[0]
    print(type(chng))
    final_amt = chng - int(pay_amt)
    print(final_amt)

    data={
        "amount":final_amt
    }

    return JsonResponse(data)