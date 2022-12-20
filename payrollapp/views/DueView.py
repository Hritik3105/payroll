from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import os
import pandas as pd
from payrollapp.models import *
import datetime
from django.core.mail import send_mail
  

@login_required 
def due_table(request):
    all_obj=Providers.objects.filter(user_id=request.user.id)
    if request.method =="POST":
        # z=os.getcwd()+"/payrollapp/csv"
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless=chrome')
        # prefs = {"download.default_directory" : z}
        # options.add_experimental_option("prefs",prefs)
                                        

        # serv_obj = Service()
        # driver = webdriver.Chrome( options=options,service = serv_obj)

        # # # Logging into LinkedIn
        # driver.get("https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/consdcvinternetui/")
        # time.sleep(3)

        # username = driver.find_element(By.ID,"rutcntr")
        # username.send_keys("767509367")  # Enter Your Email Address

        # pword = driver.find_element(By.ID,"clave")
        # pword.send_keys("market9093")        # Enter Your Password

        # driver.find_element(By.ID,"bt_ingresar").click()

        # driver.get('https://www4.sii.cl/consdcvinternetui/#/index')
        # time.sleep(3)

        # dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
        # dropdown1.select_by_visible_text('Marzo')
        # time.sleep(3)

        # dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
        # dropdown2.select_by_visible_text('2020')
        # time.sleep(3)

        # driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
        # time.sleep(3)

        # driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
        # time.sleep(3)

        filename=os.getcwd()+"/payrollapp/csv/RCV_COMPRA_REGISTRO_76750936-7_202003.csv"              
        empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
        dbframe = empexceldata
        dbframe.columns = dbframe.columns.str.replace(' ', '')
        val=dbframe.columns
        val=Providers.objects.all()
        print(len(val))
        if len(val)==0:
            print("Enter")
            for i in dbframe.itertuples():
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y")
                s = d.strftime('%Y-%m-%d')
                pro_obj=Providers()
                pro_obj.user_id=request.user.id
                pro_obj.issue_date=s
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.business_name=i.RazonSocial
                pro_obj.total_amount_paid=i.MontoTotal
                pro_obj.save()
        else:
            print("enter2")
            for i in dbframe.itertuples():
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y")
                s = d.strftime('%Y-%m-%d')
                val=Providers.objects.filter(id=request.user.id).update(issue_date=s,provider_name=i.RUTProveedor,invoice=i.Folio,business_name=i.RazonSocial,total_amount_paid=i.MontoTotal)
        return redirect("due")
    return render(request,"home/table.html",{"obj":all_obj})



