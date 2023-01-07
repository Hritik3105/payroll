import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from django.core.mail import send_mail
from django.core.mail import send_mail as sm
from payrollapp.models import Providers



def my_cron_job():
   
    res = sm(
        subject = 'Subject here',
        message = 'Hii there. I am in function',
        from_email = 'testsood981@gmail.com',
        recipient_list = ['hritik@codenomad.net'],
        fail_silently=False,
         )
   
    z='/home/nirmla/Desktop/payroll/payrollapp/csv'
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=chrome')
    prefs = {"download.default_directory" : z}
    options.add_experimental_option("prefs",prefs)
                                    

    serv_obj = Service()
    driver = webdriver.Chrome( options=options,service = serv_obj)

    # # Logging into LinkedIn
    driver.get("https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/consdcvinternetui/")
    time.sleep(8)

    username = driver.find_element(By.ID,"rutcntr")
    username.send_keys("767509367")  # Enter Your Email Address

    pword = driver.find_element(By.ID,"clave")
    pword.send_keys("market9093")        # Enter Your Password

    driver.find_element(By.ID,"bt_ingresar").click()

    driver.get('https://ww  w4.sii.cl/consdcvinternetui/#/index')
    time.sleep(6)

    dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
    dropdown1.select_by_visible_text('Marzo')
    time.sleep(6)

    dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
    dropdown2.select_by_visible_text('2022')
    time.sleep(8)

    driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
    time.sleep(3)

    driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
    time.sleep(3)

    