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
from dateutil.relativedelta import relativedelta



def get_latest_download_file(folder_path):
    files = os.listdir(folder_path)
    files = [os.path.join(folder_path, f) for f in files]
    files = [(f, os.path.getmtime(f)) for f in files]
    files = sorted(files, key=lambda x: -x[1])
    if files:
        return files[0][0]
    else:
        return None


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
    print("Entertet---------------------")
    val=calculate()
    final_path =""
    if os.path.exists("/home/ubuntu/payroll/payrollapp/"+request.user.username): 
    # if os.path.exists("/home/nirmla/Desktop/payroll/payrollapp/csv1"): 
        
        folder_path = r'/home/ubuntu/payroll/payrollapp/'+request.user.username
        # folder_path = '/home/nirmla/Desktop/payroll/payrollapp/csv1'
        file_path = get_latest_download_file(folder_path)

    
        if file_path:
           
          final_path=file_path.split(request.user.username)[1]
          pat_fnl=final_path.split(" ")[0]
    user_obj=User.objects.get(id =request.user.id)
    # input_dt = datetime.datetime(2022, 9, 13)
    # print('Input date:', input_dt.date())

  
    # next_month = input_dt.replace(day=28) + datetime.timedelta(days=4)

 
    # next_month = next_month.replace(day=28) +datetime.timedelta(days=4)

    # res = next_month - datetime.timedelta(days=next_month.day)
    # print('Last day of the next month:', res.date())


    updated_date=Providers.objects.filter(user_id=request.user.id).values_list("csv",flat=True)
    
   
    obj_pro=Providers.objects.filter(user_id=request.user.id)
    if request.method == "POST":
       
      siusername=request.POST.get("siiusername")
      username=request.POST.get("username")
      password=request.POST.get("password")  
      enddate=request.POST.get("year")
      startdate=request.POST.get("month")
      

     
      if startdate == "Enero":
        startdate1 = "01"

      if startdate == "Febrero":
        startdate1 = "02"

      if startdate == "Marzo":
        startdate1 = "03"

      if startdate == "Abril":
        startdate1 = "04"

      if startdate == "Mayo":
        startdate1 = "05"

      if startdate == "Junio":
        startdate1 = "06"

      if startdate == "Julio":
        startdate1= "07"

      if startdate == "Agosto":
        startdate1 = "08"

      if startdate == "Septiembre":
        startdate1 = "09"

      if startdate == "Octubre":
        startdate1 = "10"

      if startdate == "Noviembre":
        startdate1 = "11"

      if startdate == "Diciembre":
        startdate1 = "12"
     
      today = datetime.datetime.now()
        
      month1 = today.strftime("%m")
    
      # if "csv_pth"  in request.session:

       
      updated_date=Providers.objects.filter(user_id=request.user.id,csv=pat_fnl).values_list("created_at",flat=True)
      if updated_date:
        
        res = updated_date[0] + relativedelta(day=31)
        print("5555",res)
        print("-----------",int(startdate1))

        zz=datetime.datetime.today().replace(day=1) - datetime.timedelta(1)
        val_date=str(zz).split(" ")[0]
        pre_month=val_date.split("-")[1]
        print(int(pre_month))
        # if "2023-03 -01" != "2023-03-31" and  int(startdate1) > 3:
        last=str(updated_date[0]).split("-")
        print(last)
        valss=int(last[1])
        print(valss)
        print(int(month1))
        print(valss+1)
        curr_mon=str(updated_date[0]).split("-")[1]
        print(int(curr_mon))
        if str(updated_date[0]) != str(res) and int(startdate1) > int(valss) :


          messages.success(request,"You must update Previuos month to continue", extra_tags='suggest_upgrade')
          return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})
        elif curr_mon > pre_month and int(startdate1) < int(valss):
         

          updated_date2=Providers.objects.filter(user_id=request.user.id,csv=pat_fnl).update(is_closed=True)
          messages.success(request,"Month is already closed", extra_tags='suggest_upgrade')
        else:
        
          user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,month=startdate,year=enddate,username=username)
          sii(request,siusername,password,startdate,enddate)
          return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})
      else:

        user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,month=startdate,year=enddate,username=username)
        sii(request,siusername,password,startdate,enddate)
        return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})



      # if int(month1) > int(startdate1):
      #   messages.success(request,"you must update to continue", extra_tags='suggest_upgrade')
 
      #   return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})
    else:
      user_upd=User.objects.filter(id =request.user.id).update(siiusername=siusername,siipassword=password,month=startdate,year=enddate,username=username)
      sii(request,siusername,password,startdate,enddate)
      return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val,"val_yr":enddate,"month":startdate})
 
    return render(request,"cred/sii.html",{"user":user_obj,"obj":obj_pro,"year":val})




#DOwnload csv file 
def sii(request,siiusernae,password,month,year):
  
  try:

    
    options = webdriver.ChromeOptions()
    #download_dir = "/home/nirmla/Desktop/payroll/payrollapp/csv1"
    

    
    # paths='/home/nirmla/Desktop/payroll/payrollapp/csv1'
    options.add_argument('--headless=chrome')
    
    
    # prefs = {"download.default_directory" : paths}
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
    time.sleep(10)

    dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
    dropdown1.select_by_visible_text(month)
    time.sleep(6)

    dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
    dropdown2.select_by_visible_text(year)
    time.sleep(6)

    driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
    time.sleep(3)

    driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
    time.sleep(6)

    
    messages.success(request,"CSV Downloaded Successfull",extra_tags="company")
    time.sleep(8)


    file_exists = exists("/home/ubuntu/payroll/payrollapp/"+request.user.username)
    # # file_exists = exists("/home/nirmla/Desktop/payroll/payrollapp/csv1")
    
 
    # # directory_path="/home/nirmla/Desktop/payroll/payrollapp/csv1"
    directory_path=r'/home/ubuntu/payroll/payrollapp/'+request.user.username
    
    if file_exists == True:
    
      shutil.rmtree(directory_path, ignore_errors=True)
      shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)
      # shutil.copytree("/home/nirmla/Desktop/payroll/payrollapp/csv1", "/home/nirmla/Desktop/payroll/payrollapp/csv1")
    else:
    
      # shutil.copytree("/home/nirmla/Desktop/payroll/payrollapp/csv1", "/home/nirmla/Desktop/payroll/payrollapp/"+request.user.username)
      shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)

  except Exception as e:
    
    messages.success(request,e,extra_tags="fraud")
    

