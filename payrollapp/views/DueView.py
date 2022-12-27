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



  

@login_required 
def due_table(request):
    print(datetime.date.today())
    all_obj=Providers.objects.filter(user_id=request.user.id)
    len_obj=len(all_obj) 
    if request.method =="POST":
        filename=os.getcwd()+"/payrollapp/csv/RCV_COMPRA_REGISTRO_76750936-7_202203.csv"              
        empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
        empexceldata.columns = empexceldata.columns.str.replace(' ', '')
        val=empexceldata.columns
        val=Providers.objects.filter(user_id=request.user.id)
        
        if len(val)==0: 
            for i in empexceldata.itertuples():
                total = i.FechaDocto
                date=pd.to_datetime(total).date()
                exp=date+pd.Timedelta(days=30)
                months=pd.to_datetime(exp).month_name()
                years=exp.strftime('%Y')
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
                pro_obj=Providers()
                pro_obj.user_id=request.user.id
                pro_obj.issue_date=d
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.expiration_date=exp
                pro_obj.payment_week=4
                pro_obj.month_of_payment=months
                pro_obj.year_of_payment=years
                pro_obj.days_overdue=30
                pro_obj.business_name=i.RazonSocial
                pro_obj.total_amount_paid=i.MontoTotal
                pro_obj.year=years
                pro_obj.month=months
                pro_obj.balance_payable=0
                pro_obj.payment_policy=30
                pro_obj.amount_paid=i.MontoTotal
                pro_obj.save()        
        else:                 
           
            
            for i in empexceldata.itertuples():
                pro_obj=Providers.objects.filter(user_id=request.user.id)    
                total = i.FechaDocto
                date=pd.to_datetime(total).date()
                exp=date+pd.Timedelta(days=30)
                months=pd.to_datetime(exp).month_name()
                years=exp.strftime('%Y')
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')                                                                                               
                pro_obj.user_id=request.user.id
                pro_obj.issue_date=d
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.expiration_date=exp
                pro_obj.payment_week=4
                pro_obj.month_of_payment=months
                pro_obj.year_of_payment=years
                pro_obj.days_overdue=30
                pro_obj.business_name=i.RazonSocial
                pro_obj.total_amount_paid=i.MontoTotal
                pro_obj.year=years
                pro_obj.month=months
                pro_obj.balance_payable=0
                pro_obj.payment_policy=30
                pro_obj.amount_paid=i.MontoTotal
          
                # print("enter")
                # total = i.FechaDocto
                # date=pd.to_datetime(total).date()
                # exp=date+pd.Timedelta(days=30)
                # months=pd.to_datetime(exp).month_name()
                # years=exp.strftime('%Y')
                # d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
        #         val=Providers.objects.filter(user_id=request.user.id).update(issue_date=d,provider_name=i.RUTProveedor,invoice=i.Folio,business_name=i.RazonSocial,total_amount_paid=i.MontoTotal,expiration_date=exp,payment_week=4,month_of_payment=months,year_of_payment=years,days_overdue=30,balance_payable=0,amount_paid=i.MontoTotal,month=months,year=years,payment_policy=30)
        return redirect("due")
    return render(request,"home/table.html",{"obj":all_obj,"len":len_obj})



