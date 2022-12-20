from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from django.shortcuts import render,redirect


def downloadcsv(request):

    if request.method=="POST":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=chrome')
                                        

        serv_obj = Service()
        driver = webdriver.Chrome( options=options,service = serv_obj)

        # # Logging into LinkedIn
        driver.get("https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/consdcvinternetui/")
        time.sleep(5)

        username = driver.find_element(By.ID,"rutcntr")
        username.send_keys("767509367")  # Enter Your Email Address

        pword = driver.find_element(By.ID,"clave")
        pword.send_keys("market9093")        # Enter Your Password

        driver.find_element(By.ID,"bt_ingresar").click()

        driver.get('https://www4.sii.cl/consdcvinternetui/#/index')
        time.sleep(5)

        dropdown1 = Select(driver.find_element(By.ID,'periodoMes'))
        dropdown1.select_by_visible_text('Noviembre')
        time.sleep(5)

        dropdown2 = Select(driver.find_element(By.XPATH,"//select[@ng-model='periodoAnho']"))
        dropdown2.select_by_visible_text('2020')
        time.sleep(5)

        driver.find_element(By.CLASS_NAME,"btn.btn-default.btn-xs-block.btn-block").click()
        time.sleep(5)

        driver.find_element(By.XPATH,"//button[text()='Descargar Detalles']").click()
        time.sleep(5)
        return redirect("siiview")

    return render(request,"sii/downcsv.html")    

