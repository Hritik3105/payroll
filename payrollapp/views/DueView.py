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
import os
import shutil
from os.path import exists




#get latest download file

'''Get the latest file from  a Folder'''


def get_latest_download_file(folder_path):
    files = os.listdir(folder_path)
    files = [os.path.join(folder_path, f) for f in files]
   
    files = [(f, os.path.getmtime(f)) for f in files]
    
    files = sorted(files, key=lambda x: -x[1])
    if files:
        return files[0][0]
    else:
        return None




# function to insert data

'''Get the csv data and insert it into database to use further'''
@login_required 
def due_table(request):
    final_path =""
    if os.path.exists("/home/ubuntu/payroll/payrollapp/"+request.user.username): 
    # if os.path.exists("/home/nirmla/Desktop/payroll/payrollapp/csv1"): 
        folder_path = r'/home/ubuntu/payroll/payrollapp/'+request.user.username
        # folder_path = '/home/nirmla/Desktop/payroll/payrollapp/csv1'
        file_path = get_latest_download_file(folder_path)
        if file_path:
            final_path=file_path.split(request.user.username)[1]
            # final_path=file_path.split("csv1")[1]
            updt=final_path.split(" ")[0]
            request.session["csv_pth"]=updt
            # final_path=file_path.split("csv1")[1]
            final_path=file_path.split(request.user.username)[1]
    all_obj=Providers.objects.filter(user_id=request.user.id)
    len_obj=len(all_obj) 
    if final_path:
        if request.method =="POST" and  'due' in request.POST:
            filename=os.getcwd()+"/payrollapp/" +request.user.username + final_path
            # filename=os.getcwd()+"/payrollapp/csv1"  + final_path 
            chng=Providers.objects.filter(user_id=request.user.id).values_list("csv",flat=True)
            x=final_path.split(" ")[0]
            lst=[]
            for i in chng:
                z=i.split(" ")
                lst.append(z[0])
            if x  not in lst :
                files = os.listdir(folder_path)
                files = [os.path.join(folder_path, f) for f in sorted(files)]
                for cv_fl in files: 
                    empexceldata = pd.read_csv(cv_fl,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
                    zz=empexceldata.drop_duplicates(subset='Folio', keep="first")
                    zz.columns = empexceldata.columns.str.replace(' ', '')
                    val=zz.columns
                    for i in zz.itertuples():
                        z=Providers.objects.filter(user_id =request.user.id)
                        total = i.FechaDocto
                        Begindate = datetime.datetime.strptime(total,"%d/%m/%Y").strftime('%Y-%m-%d')
                        date=pd.to_datetime(Begindate).date()
                        exp=date+pd.Timedelta(days=30)
                        date_format1 = "%Y-%m-%d"
                        date1 = datetime.datetime.strptime(str(date), date_format1)
                        exp2 = datetime.datetime.strptime(str(exp), date_format1)
                        week2=exp2 - date1
                        weeks=exp2.day/4
                        week=exp.day/4
                        months=pd.to_datetime(exp).month_name()
                        years=exp.strftime('%Y')
                        d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
                        date_format = "%Y-%m-%d"
                        a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                        b = datetime.datetime.strptime(str(d), date_format)
                        today= a-b 
                        pro_obj=Providers()
                        final_csv_path=cv_fl.split(request.user.username)[1]
                        pro_obj.csv=final_csv_path.split(" ")[0]
                        pro_obj.user_id=request.user.id
                        pro_obj.issue_date=d
                        pro_obj.provider_name=i.RUTProveedor
                        pro_obj.invoice=i.Folio
                        pro_obj.expiration_date=exp
                        if exp2.day/4 >=0 and exp2.day/4 <=1.75:
                            pro_obj.payment_week=1
                        elif exp2.day/4 >1.75 and exp2.day/4 <= 3.75:
                            pro_obj.payment_week=2
                        elif exp2.day/4 > 3.75 and exp2.day/4 <=5.75:
                            pro_obj.payment_week=3
                        elif exp2.day/4 >5.75 and exp2.day/4 <=7.75:
                            pro_obj.payment_week=4
                        pro_obj.month_of_payment=months
                        pro_obj.year_of_payment=years
                        pro_obj.days_overdue=today.days
                        pro_obj.business_name=i.RazonSocial    
                        if numpy.isnan(i.MontoTotal):
                            pro_obj.total_amount_paid=0
                        else:   
                            pro_obj.total_amount_paid=int(i.MontoTotal)
                        pro_obj.week=weeks
                        pro_obj.year=years
                        pro_obj.month=months
                        pro_obj.balance_payable=0
                        pro_obj.payment_policy=30
                        pro_obj.payment_term=30
                        if numpy.isnan(i.MontoTotal):
                            pro_obj.amount_paid=0
                        else:   
                            pro_obj.amount_paid=int(i.MontoTotal)
                        pro_obj.save()  
                shutil.rmtree("/home/ubuntu/payroll/payrollapp/"+request.user.username)
                os.mkdir("/home/ubuntu/payroll/payrollapp/"+request.user.username)
                shutil.rmtree("/home/ubuntu/Downloads")
                os.mkdir("/home/ubuntu/Downloads")
                return redirect("due")
            else:
                Providers.objects.filter(user_id=request.user.id,csv=x).delete()
                empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
                zz=empexceldata.drop_duplicates(subset='Folio', keep="first")                
                zz.columns = empexceldata.columns.str.replace(' ', '')
                val=zz.columns
                for i in zz.itertuples():
                    z=Providers.objects.filter(user_id =request.user.id) 
                    total = i.FechaDocto
                    Begindate = datetime.datetime.strptime(total,"%d/%m/%Y").strftime('%Y-%m-%d')
                    date=pd.to_datetime(Begindate).date()
                    exp=date+pd.Timedelta(days=30)
                    date_format1 = "%Y-%m-%d"                    
                    date1 = datetime.datetime.strptime(str(date), date_format1)
                    exp2 = datetime.datetime.strptime(str(exp), date_format1)  
                    week2=exp2 - date1
                    weeks=exp2.day/4
                    week=exp.day/4
                    months=pd.to_datetime(exp).month_name()
                    years=exp.strftime('%Y')
                    d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
                    date_format = "%Y-%m-%d"
                    a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                    b = datetime.datetime.strptime(str(d), date_format)
                    today= a-b
                    pro_obj=Providers()
                    pro_obj.csv=x
                    pro_obj.user_id=request.user.id
                    pro_obj.issue_date=d
                    pro_obj.provider_name=i.RUTProveedor
                    pro_obj.invoice=i.Folio
                    pro_obj.expiration_date=exp
                    if exp2.day/4 >=0 and exp2.day/4 <=1.75:
                        pro_obj.payment_week=1
                    elif exp2.day/4 >1.75 and exp2.day/4 <= 3.75:
                        pro_obj.payment_week=2
                    elif exp2.day/4 > 3.75 and exp2.day/4 <=5.75:
                        pro_obj.payment_week=3  
                    elif exp2.day/4 >5.75 and exp2.day/4 <=7.75:
                        pro_obj.payment_week=4
                    pro_obj.month_of_payment=months
                    pro_obj.year_of_payment=years
                    pro_obj.days_overdue=today.days
                    pro_obj.business_name=i.RazonSocial    
                    if numpy.isnan(i.MontoTotal):
                        pro_obj.total_amount_paid=0
                    else:   
                        pro_obj.total_amount_paid=int(i.MontoTotal)
                    pro_obj.week=weeks
                    pro_obj.year=years
                    pro_obj.month=months
                    pro_obj.balance_payable=0
                    pro_obj.payment_policy=30
                    pro_obj.payment_term=30
                    if numpy.isnan(i.MontoTotal):
                        pro_obj.amount_paid=0
                    else:   
                        pro_obj.amount_paid=int(i.MontoTotal)
                    pro_obj.save()    
                shutil.rmtree("/home/ubuntu/payroll/payrollapp/"+request.user.username)
                os.mkdir("/home/ubuntu/payroll/payrollapp/"+request.user.username) 
                shutil.rmtree("/home/ubuntu/Downloads")
                os.mkdir("/home/ubuntu/Downloads")   
                return redirect("due")
        if request.method =="POST" and "manual" in request.POST:
            val=request.FILES.get("image")   
            lst=[]
            zz=Providers.objects.filter(user_id=request.user.id).values_list("invoice",flat=True)
            for i in zz:
                lst.append(int(i))    
            if val:
                filenames=val    
                empexceldata = pd.read_csv(filenames,error_bad_lines=False,sep=r';')
                dup=empexceldata.drop_duplicates(subset='Folio', keep="first")
                dup.columns = dup.columns.str.replace(' ', '')
                val=dup.columns    
                for i in dup.itertuples():
                    testeddate = i.FechaDocto
                    dt_obj = datetime.datetime.strptime(testeddate,'%d-%m-%y')
                    valll=datetime.datetime.strftime(dt_obj,'%Y-%m-%d')
                    date_format = "%Y-%m-%d"
                    a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                    b = datetime.datetime.strptime(str(valll), date_format)
                    today= a-b      
                    total = i.FechaDocto
                    date=pd.to_datetime(total).date()
                    exp=date+pd.Timedelta(days=30)
                    mon=pd.to_datetime(exp).month_name()
                    yea=exp.strftime('%Y')
                    date_format1 = "%Y-%m-%d"  
                    date1 = datetime.datetime.strptime(str(date), date_format1)
                    exp2 = datetime.datetime.strptime(str(exp), date_format1)
                    week2=exp2 - date1
                    weeks=exp2.day/4
                    week=exp.day/4
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
                    if exp2.day/4 >=0 and exp2.day/4 <=1.75:
                        pro_obj.payment_week=1
                    elif exp2.day/4 >1.75 and exp2.day/4 <= 3.75:
                        pro_obj.payment_week=2
                    elif exp2.day/4 > 3.75 and exp2.day/4 <=5.75:
                        pro_obj.payment_week=3
                    elif exp2.day/4 >5.75 and exp2.day/4 <=7.75:
                        pro_obj.payment_week=4
                    pro_obj.week=weeks
                    
                    if numpy.isnan(i.MontoTotal):
                        pro_obj.amount_paid=0
                    else:   
                        pro_obj.total_amount_paid=int(i.MontoTotal)
                    if numpy.isnan(i.MontoTotal):
                        pro_obj.amount_paid=0
                    else:   
                        pro_obj.amount_paid=int(i.MontoTotal)
                    if i.Folio in lst:
                        print("--------------------",i.Folio)
                    else:      
                        pro_obj.save()
                return redirect("due")
            return redirect("due")      
        return render(request,"home/table.html",{"obj":all_obj,"len":len_obj})
    else:
        all_obj=Providers.objects.filter(user_id=request.user.id)
        len_obj=len(all_obj) 
        return render(request,"home/table.html",{"obj":all_obj,"len":len_obj})        



#function to updade data

def update(request):
    try:  

        currentMonth = datetime.datetime.now()
        curr_name=currentMonth.strftime("%B")
        if  "January"  in curr_name:
          curr_name = "Enero"

        if  "february" in curr_name:
          curr_name = "Febrero"

        if   "March" in curr_name:
          curr_name = "Marzo"

        if  "April" in curr_name:
          curr_name = "Abril"

        if  "May" in curr_name:
          curr_name = "Mayo"

        if  "June" in curr_name:
          curr_name = "Junio"

        if  "July" in curr_name:
          curr_name= "Julio"

        if  "August" in curr_name:
          curr_name = "Agosto"

        if "September" in curr_name:
          curr_name = "Septiembre"

        if "October" in curr_name:
          curr_name = "Octubre"

        if  "November" in curr_name:
          curr_name = "Noviembre"

        if  "December" in curr_name:
          curr_name = "Diciembre"

        currentYear = datetime.datetime.now().year
       
        options = webdriver.ChromeOptions()
        
        options.add_argument('--headless=chrome')
        
        
        serv_obj = Service()
        driver = webdriver.Chrome(options=options,service = serv_obj)

        # # Logging into LinkedIn
        driver.get("https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/consdcvinternetui/")
        time.sleep(8)


        sii_value=User.objects.filter(id=request.user.id).values("siipassword","siiusername")

        sii_pass=sii_value[0]["siipassword"]
        sii_user=sii_value[0]["siiusername"]


        username = driver.find_element(By.ID,"rutcntr")
        username.send_keys(sii_user)  # Enter Your Email Address #767509367

        pword = driver.find_element(By.ID,"clave")
        pword.send_keys(sii_pass)        # Enter Your Password #market9093

        driver.find_element(By.ID,"bt_ingresar").click()

        driver.get('https://www4.sii.cl/consdcvinternetui/#/index')
        time.sleep(10)

        dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
        dropdown1.select_by_visible_text(curr_name)
        time.sleep(6)

        dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
        dropdown2.select_by_visible_text(str(currentYear))
        time.sleep(6)

        driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
        time.sleep(3)

        driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
        time.sleep(6)
    

        files_download = os.listdir("/home/ubuntu/Downloads")
        
        
        for i in files_download:
           
            if len(i) >41: 
                os.remove("/home/ubuntu/Downloads/" + i)
            
            
                    
        file_exists = exists("/home/ubuntu/payroll/payrollapp/"+request.user.username)
     
    
       
        directory_path=r'/home/ubuntu/payroll/payrollapp/'+request.user.username
        
        if file_exists == True:
     
            shutil.rmtree(directory_path, ignore_errors=True)
            shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)
            folder_path = r'/home/ubuntu/payroll/payrollapp/'+request.user.username
            file_path = get_latest_download_file(folder_path)
            if file_path:

                
                final_path=file_path.split(request.user.username)[1]
            x=final_path.split(" ")[0]
            filename=os.getcwd()+"/payrollapp/"+request.user.username +final_path     
            Providers.objects.filter(user_id=request.user.id,csv=x).delete()
            empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
            zz=empexceldata.drop_duplicates(subset='Folio', keep="first")
            
            zz.columns = empexceldata.columns.str.replace(' ', '')
            val=zz.columns

            for i in zz.itertuples():
                z=Providers.objects.filter(user_id =request.user.id)
        
                
                total = i.FechaDocto
                
                
                Begindate = datetime.datetime.strptime(total,"%d/%m/%Y").strftime('%Y-%m-%d')
                date=pd.to_datetime(Begindate).date()
                exp=date+pd.Timedelta(days=30)
                
                date_format1 = "%Y-%m-%d"
                
                date1 = datetime.datetime.strptime(str(date), date_format1)
                exp2 = datetime.datetime.strptime(str(exp), date_format1)
                
                week2=exp2 - date1
                weeks=exp2.day/4

                week=exp.day/4
                months=pd.to_datetime(exp).month_name()
                years=exp.strftime('%Y')
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
                date_format = "%Y-%m-%d"
                a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                b = datetime.datetime.strptime(str(d), date_format)
                today= a-b

    
                pro_obj=Providers()
                pro_obj.csv=x
                
                pro_obj.user_id=request.user.id
                pro_obj.issue_date=d
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.expiration_date=exp
                if exp2.day/4 >=0 and exp2.day/4 <=1.75:
                    pro_obj.payment_week=1
                elif exp2.day/4 >1.75 and exp2.day/4 <= 3.75:
                    pro_obj.payment_week=2
                elif exp2.day/4 > 3.75 and exp2.day/4 <=5.75:
                    pro_obj.payment_week=3  
                elif exp2.day/4 >5.75 and exp2.day/4 <=7.75:
                    pro_obj.payment_week=4
                pro_obj.month_of_payment=months
                pro_obj.year_of_payment=years
                pro_obj.days_overdue=today.days
                pro_obj.business_name=i.RazonSocial    
                if numpy.isnan(i.MontoTotal):
                    pro_obj.total_amount_paid=0
                else:   
                    pro_obj.total_amount_paid=int(i.MontoTotal)
                pro_obj.week=weeks
                pro_obj.year=years
                pro_obj.month=months
                pro_obj.balance_payable=0
                pro_obj.payment_policy=30
                pro_obj.payment_term=30
                if numpy.isnan(i.MontoTotal):
                    pro_obj.amount_paid=0
                else:   
                    pro_obj.amount_paid=int(i.MontoTotal)
                pro_obj.save()    
            shutil.rmtree("/home/ubuntu/payroll/payrollapp/"+request.user.username)
            os.mkdir("/home/ubuntu/payroll/payrollapp/"+request.user.username) 
            shutil.rmtree("/home/ubuntu/Downloads")
            os.mkdir("/home/ubuntu/Downloads")   
            return redirect("due")
        
        else:
           
           
            shutil.copytree("/home/ubuntu/Downloads", "/home/ubuntu/payroll/payrollapp/"+request.user.username)
            folder_path = r'/home/ubuntu/payroll/payrollapp/'+request.user.username
            file_path = get_latest_download_file(folder_path)
            if file_path:

                
                final_path=file_path.split(request.user.username)[1]
            x=final_path.split(" ")[0]
            filename=os.getcwd()+"/payrollapp/"+request.user.username +final_path     
            Providers.objects.filter(user_id=request.user.id,csv=x).delete()
            empexceldata = pd.read_csv(filename,error_bad_lines=False,sep=r';',usecols =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
            zz=empexceldata.drop_duplicates(subset='Folio', keep="first")
            
            zz.columns = empexceldata.columns.str.replace(' ', '')
            val=zz.columns

            for i in zz.itertuples():
                z=Providers.objects.filter(user_id =request.user.id)
        
                
                total = i.FechaDocto
                
                
                Begindate = datetime.datetime.strptime(total,"%d/%m/%Y").strftime('%Y-%m-%d')
                date=pd.to_datetime(Begindate).date()
                exp=date+pd.Timedelta(days=30)
                
                date_format1 = "%Y-%m-%d"
                
                date1 = datetime.datetime.strptime(str(date), date_format1)
                exp2 = datetime.datetime.strptime(str(exp), date_format1)
                
                week2=exp2 - date1
                weeks=exp2.day/4

                week=exp.day/4
                months=pd.to_datetime(exp).month_name()
                years=exp.strftime('%Y')
                d = datetime.datetime.strptime(i.FechaDocto,"%d/%m/%Y").strftime('%Y-%m-%d')
                date_format = "%Y-%m-%d"
                a = datetime.datetime.strptime(str(datetime.datetime.now().date()), date_format)
                b = datetime.datetime.strptime(str(d), date_format)
                today= a-b

    
                pro_obj=Providers()
                pro_obj.csv=x
                
                pro_obj.user_id=request.user.id
                pro_obj.issue_date=d
                pro_obj.provider_name=i.RUTProveedor
                pro_obj.invoice=i.Folio
                pro_obj.expiration_date=exp
                if exp2.day/4 >=0 and exp2.day/4 <=1.75:
                    pro_obj.payment_week=1
                elif exp2.day/4 >1.75 and exp2.day/4 <= 3.75:
                    pro_obj.payment_week=2
                elif exp2.day/4 > 3.75 and exp2.day/4 <=5.75:
                    pro_obj.payment_week=3  
                elif exp2.day/4 >5.75 and exp2.day/4 <=7.75:
                    pro_obj.payment_week=4
                pro_obj.month_of_payment=months
                pro_obj.year_of_payment=years
                pro_obj.days_overdue=today.days
                pro_obj.business_name=i.RazonSocial    
                if numpy.isnan(i.MontoTotal):
                    pro_obj.total_amount_paid=0
                else:   
                    pro_obj.total_amount_paid=int(i.MontoTotal)
                pro_obj.week=weeks
                pro_obj.year=years
                pro_obj.month=months
                pro_obj.balance_payable=0
                pro_obj.payment_policy=30
                pro_obj.payment_term=30
                if numpy.isnan(i.MontoTotal):
                    pro_obj.amount_paid=0
                else:   
                    pro_obj.amount_paid=int(i.MontoTotal)
                pro_obj.save()    
            shutil.rmtree("/home/ubuntu/payroll/payrollapp/"+request.user.username)
            os.mkdir("/home/ubuntu/payroll/payrollapp/"+request.user.username) 
            shutil.rmtree("/home/ubuntu/Downloads")
            os.mkdir("/home/ubuntu/Downloads")   
            return redirect("due")


    except Exception as e:
        
        
        return redirect("due")