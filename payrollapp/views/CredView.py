from django.shortcuts import render,redirect,HttpResponse
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
import shutil
from os.path import exists
import pathlib
import requests




#Function used to get year
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




# Function to enter SII Credential
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
     
      enddate=request.POST.get("year")  
     
        
      user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,month=startdate,year=enddate,username=username)
      sii(request,siusername,password,startdate,enddate)
      return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})

    return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val})




#DOwnload csv file 
def sii(request,siiusernae,password,month,year):
  
  try:
    # z='/home/nirmla/Desktop/payroll/payrollapp/csv'
    options = webdriver.ChromeOptions()


    options.add_argument('--headless=chrome')
    options.add_argument('--disable-gpu')  
    # prefs = {"download.default_directory" : "/home/nirmla/Desktop/payroll/payrollapp/csv"}
    # options.add_experimental_option("prefs",prefs)

                                  
    
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
    time.sleep(8)

    dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
    dropdown1.select_by_visible_text(month)
    time.sleep(6)

    dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
    dropdown2.select_by_visible_text(year)
    time.sleep(6)

    driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
    time.sleep(3)

    driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
    time.sleep(3)
    file_name = driver.current_url.split("/")[-1]
    print("345467",file_name)
    

   
    messages.success(request,"CSV Downloaded Successfull",extra_tags="company")
    time.sleep(10)


    file_exists = exists("/home/ubuntu/payroll/payrollapp/"+request.user.username)
    # file_exists = exists("/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username)
    
 
    # directory_path="/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username
    directory_path=r'/home/ubuntu/payroll/payrollapp/'+request.user.username
    
    if file_exists == True:
      print("true")
      shutil.rmtree(directory_path, ignore_errors=True)
      shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)
      # shutil.copytree("/home/nirmla/Desktop/payroll/payrollapp/csv", "/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username)
    else:
      print("hello")
      # shutil.copytree("/home/nirmla/Desktop/payroll/payrollapp/csv", "/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username)
      shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)

  except Exception as e:
    
    messages.success(request,e,extra_tags="fraud")
    

