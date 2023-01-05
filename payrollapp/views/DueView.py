from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import os
import pandas as pd
from payrollapp.models import *
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import numpy


def covid_data(request):                                                          
      vas= Providers.objects.filter(user_id=request.user.id)     
      vas1="hritjklhgkjh"                                                                
      return vas,vas1
  
#insert data
@login_required 
def due_table(request):
    print(datetime.date.today())
    all_obj=Providers.objects.filter(user_id=request.user.id)
    len_obj=len(all_obj) 
    if request.method =="POST" and  'due' in request.POST:
        filename=os.getcwd()+"/payrollapp/csv/RCV_COMPRA_REGISTRO_76750936-7_202203.csv"              
        empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
        empexceldata.columns = empexceldata.columns.str.replace(' ', '')
        val=empexceldata.columns
        val=Providers.objects.filter(user_id=request.user.id)
        
        
        for i in empexceldata.itertuples():
            total = i.FechaDocto
            date=pd.to_datetime(total).date()
            exp=date+pd.Timedelta(days=30)
            months=pd.to_datetime(exp).month_name()
            years=exp.strftime('%Y')
            d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
            date_format = "%Y-%m-%d"
            a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
            b = datetime.datetime.strptime(str(d), date_format)
            today= a-b
            
            pro_obj=Providers()
            pro_obj.user_id=request.user.id
            pro_obj.issue_date=d
            pro_obj.provider_name=i.RUTProveedor
            pro_obj.invoice=i.Folio
            pro_obj.expiration_date=exp
            pro_obj.payment_week=4
            pro_obj.month_of_payment=months
            pro_obj.year_of_payment=years
            pro_obj.days_overdue=today.days
            pro_obj.business_name=i.RazonSocial    
            if numpy.isnan(i.MontoTotal):
                pro_obj.total_amount_paid=0
            else:   
                pro_obj.total_amount_paid=int(i.MontoTotal)
            
            pro_obj.year=years
            pro_obj.month=months
            pro_obj.balance_payable=0
            pro_obj.payment_policy=30
            if numpy.isnan(i.MontoTotal):
                pro_obj.amount_paid=0
            else:   
                pro_obj.amount_paid=int(i.MontoTotal)
            pro_obj.save()        
        return redirect("due")
    if request.method =="POST" and "manual" in request.POST:
        q=covid_data(request)
        
        print("ddddddddddddddddddddddddddddddddg",q)
        val=request.FILES.get("image")
        if val:
            filenames=val    
            empexceldata = pd.read_csv(filenames,error_bad_lines=False,sep=r';')
            empexceldata.columns = empexceldata.columns.str.replace(' ', '')
            val=empexceldata.columns
            for i in empexceldata.itertuples():
                testeddate = i.FechaDocto
                dt_obj = datetime.datetime.strptime(testeddate,'%d-%m-%y')
                valll=datetime.datetime.strftime(dt_obj,'%Y-%m-%d')
                print(valll)
                date_format = "%Y-%m-%d"
                a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                b = datetime.datetime.strptime(str(valll), date_format)
                today= a-b      
                total = i.FechaDocto
                date=pd.to_datetime(total).date()
                exp=date+pd.Timedelta(days=30)
                mon=pd.to_datetime(exp).month_name()
                yea=exp.strftime('%Y')
            

                pro_obj=Providers()

                pro_obj.user_id=request.user.id
                pro_obj.issue_date=valll
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.business_name=i.RazonSocial  
                pro_obj.balance_payable=0  
                pro_obj.year_of_payment=yea
                pro_obj.expiration_date=exp
                pro_obj.month_of_payment=mon
                pro_obj.days_overdue=today.days
                pro_obj.payment_week=4
                
                if numpy.isnan(i.MontoTotal):
                    pro_obj.amount_paid=0
                else:   
                    pro_obj.total_amount_paid=int(i.MontoTotal)
                if numpy.isnan(i.MontoTotal):
                    pro_obj.amount_paid=0
                else:   
                    pro_obj.amount_paid=int(i.MontoTotal)
                pro_obj.save()
            return redirect("due")
        return redirect("due")

        
    return render(request,"home/table.html",{"obj":all_obj,"len":len_obj})


#updade data
vals=[]
def update(request):
    filename=os.getcwd()+"/payrollapp/csv/RCV_COMPRA_REGISTRO_76750936-7_202203.csv"              
    empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
    empexceldata.columns = empexceldata.columns.str.replace(' ', '')
    val=empexceldata.columns
    zz=Providers.objects.all()
    ids = []                 
    zz=Providers.objects.all().values_list("id",flat =True)
    for i in zz:
        ids.append(i)
    count = 0
    for i in empexceldata.itertuples():
        total = i.FechaDocto
        date=pd.to_datetime(total).date()
        exp=date+pd.Timedelta(days=30)
        months=pd.to_datetime(exp).month_name()
        years=exp.strftime('%Y')
        d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
        date_format = "%Y-%m-%d"
        a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
        b = datetime.datetime.strptime(str(d), date_format)
        today= a-b      
        Providers.objects.filter(id=ids[count]).update(user_id=request.user.id,days_overdue=today.days,issue_date=d,provider_name=i.RUTProveedor,invoice=i.Folio,expiration_date=exp,payment_week=4,month_of_payment=months,year_of_payment=years,business_name=i.RazonSocial,year=years,month=months,balance_payable=0,payment_policy=30)
        count +=1
    return redirect("due")


