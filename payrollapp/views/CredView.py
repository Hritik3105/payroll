from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payrollapp.models import *
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os
import datetime
from django.contrib import messages



def calculate():
    lst=[]
    lst2=[]
    today = datetime.date.today()
    year = today.year
    val1=year-6
    val4=year
    for i in range(int(val1),int(val4)+1):
      lst.append(str(i))

 
    return lst


@login_required 
def credential(request):
    val=calculate()
    user_obj=User.objects.get(id =request.user.id)
    
    obj_pro=Providers.objects.filter(user_id=request.user.id)
    if request.method == "POST":
       
      siusername=request.POST.get("siiusername")
      username=request.POST.get("username")
      password=request.POST.get("password")  
      
      startdate=request.POST.get("month")
      print(startdate)
      enddate=request.POST.get("year")  
      print(enddate)
      user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,month=startdate,year=enddate,username=username)
      sii(request,siusername,password,startdate,enddate)
      return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})

    return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val})


def sii(request,siiusernae,password,month,year):
  
  try:
  
    z='/home/nirmla/Desktop/payroll/payrollapp/csv'
    

    
    
  
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')
    prefs = {"download.default_directory" : z}
    options.add_experimental_option("prefs",prefs)
                                    

    serv_obj = Service()
    driver = webdriver.Chrome(options=options,service = serv_obj)

    # # Logging into LinkedIn
    driver.get("https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/consdcvinternetui/")
    time.sleep(8)

    username = driver.find_element(By.ID,"rutcntr")
    username.send_keys(siiusernae)  # Enter Your Email Address #767509367

    pword = driver.find_element(By.ID,"clave")
    pword.send_keys(password)        # Enter Your Password #market9093

    driver.find_element(By.ID,"bt_ingresar").click()

    driver.get('https://www4.sii.cl/consdcvinternetui/#/index')
    time.sleep(10)

    dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
    dropdown1.select_by_visible_text(month)
    time.sleep(8)

    dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
    dropdown2.select_by_visible_text(year)
    time.sleep(8)

    driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
    time.sleep(3)

    driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
    time.sleep(3)
    messages.success(request,"CSV Downloaded Successfull",extra_tags="company")

  except Exception as e:
    
    messages.success(request,e,extra_tags="fraud")
    