from contextlib import nullcontext
from typing import Generic
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Compte
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.urls import reverse
import random
import time
import datetime
from selenium.webdriver.support.ui import Select
import pandas as pd
import matplotlib.pyplot as plt
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Create your views here.
def accueil(request) :
    if Compte.objects.filter(connecte = True).count() != 0:
         c = Compte.objects.get(connecte = True)
         c.connecte = False
         c.save(update_fields=["connecte"])
    return render(request, 'accueil.html')

def inscription(request) :
    return render(request, 'inscription.html')

def connexion(request):
    return render(request, 'connexion.html')

def NewAccueil(request):
    return render(request, 'newAccueil.html')

def login(request):
    if request.method == "POST" :
        emailform = request.POST.get("email")
        mdpform = request.POST.get("mdp")
        if Compte.objects.filter(email = emailform, password = mdpform).count() == 0 :
            return render(request, 'connexion.html', {"message1" : "email et/ou mot de passe incorrect(s)"})
        elif Compte.objects.get(email = emailform, password = mdpform).email_verifie == False :
            return render(request, 'connexion.html', {"message1" : "Email non vérifié"}) 
        else :
            c = Compte.objects.get(email = emailform, password = mdpform)
            c.connecte = True
            c.save(update_fields=["connecte"])
            return redirect('NewAccueil')            


def activation(request):
     if request.method == "POST" :
        idenform = request.POST.get("iden")
        if Compte.objects.filter(identifiant = idenform).count() == 0 :
            return render(request, 'activate.html', {"message1" : "Utilisateur non existant"})
        elif Compte.objects.filter(identifiant = idenform, email_verifie = False).count() != 0 :
            c = Compte.objects.get(identifiant = idenform)
            c.email_verifie = True
            c.save(update_fields=["email_verifie"])
            return render(request, 'activate.html', {"message1" : "Compte vérifié"})          

def newUser(request):
    nomform = request.POST.get("nom")
    prenomform = request.POST.get("prenom")
    datedenaissanceform = request.POST.get("datedenaissance")
    emailform = request.POST.get("email")
    mdpform = request.POST.get("mdp")
    mdp1form = request.POST.get("mdp1")
    ident = random.randint(1,10000)
    if (Compte.objects.filter(nom = nomform, prenom = prenomform).count() != 0) :
        return render(request, 'inscription.html', {"message2" : "utilisateur déjà existant"})
    elif  (Compte.objects.filter(email = emailform).count() != 0) :
        return render(request, 'inscription.html', {"message2" : "email déjà utilisé"})
    elif (mdpform == mdp1form) :
        newCompte = Compte(nom = nomform, prenom = prenomform, email = emailform , password = mdpform,birthday = datedenaissanceform, connecte = False, identifiant = ident)
        email = EmailMessage(
            'Activer votre compte',
            'Veuillez fournir ce code de vérification : ' + str(ident),
            'othmanefarah@hotmail.com',
            [emailform],
        )
        email.send(fail_silently = False)
        newCompte.save()
        return render(request, 'activate.html', {"message1" : "consulter votre boite mail"})
    else :
        return render(request, 'inscription.html', {"message2" : "mot de passe différents"})

def simulation(request):
    codeform = request.POST.get("code")
    consommationform = request.POST.get("consommation")
    datefinform = request.POST.get("datefin")
    datedebutform = request.POST.get("datedebut")

    latitudeform = request.POST.get("latitude")
    longitudeform = request.POST.get("longitude")
    rayoform = request.POST.get("rayo")
    datefinform1 = request.POST.get("datefin1")
    datedebutform1 = request.POST.get("datedebut1")
    inclinaisonform = request.POST.get("inclinaison")
    azimutform = request.POST.get("azimut")


    URL = "https://data.enedis.fr/page/coefficients-des-profils/?flg=fr"
    option = Options()
    preferences = {"download.default_directory": "C:\data"}
    option.add_experimental_option("prefs",preferences)
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options = option, service = s)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(URL)
    #driver.switch_to.frame(0)
    driver.find_element(By.CSS_SELECTOR, ".ng-pristine").click()
    Select(driver.find_element(By.XPATH,  "//*/div/div/div/div/div/ods-dataset-context/div[1]/div[3]/div/select")).select_by_value(""+codeform+"")
    a3 = driver.find_element(By.XPATH, "//*/div/div/div/div/div/ods-dataset-context/div[1]/div[4]/div[1]/input")
    a3.clear()
    a3.send_keys(datedebutform)
    a4 = driver.find_element(By.XPATH, "//*/div/div/div/div/div/ods-dataset-context/div[1]/div[4]/div[2]/input")
    a4.clear()
    a4.send_keys(datefinform)
    driver.find_element(By.XPATH, "//*/div/div/div/div/div/ods-dataset-context/div[1]").click()
    driver.find_element(By.XPATH, "//*/div/div/div/div/div/ods-dataset-context/div[2]/a[1]/i").click()
    while(not os.path.exists("C:\data\coefficients-des-profils.csv")) :
        None
    file = pd.read_csv("C:\data\coefficients-des-profils.csv",sep=";")
    file = file.drop(columns=['COEFFICIENT_PREPARE','COEFFICIENT_DYNAMIQUE','SOUS_PROFIL','CATEGORIE'],axis = 1)
    somme = file['COEFFICIENT_AJUSTE'].sum()
    file['newCol'] = (float(consommationform)/somme) *  file['COEFFICIENT_AJUSTE']
    file = file.drop(columns=['COEFFICIENT_AJUSTE'],axis = 1)
    file = file.sort_values('HORODATE')
    list1 = file['HORODATE'].to_list()
    for i in range(len(list1)) :
        newstr = (list1[i].split("T")[0]).split("-")
        newstr1 = (list1[i].split("T")[1]).split("+")[0].split(":")
        list1[i] = newstr[0]+newstr[1]+newstr[2]+":"+newstr1[0]+newstr1[1]
    list1 = [list1[i] for i in range (len(list1)) if list1[i].split(":")[1][2] != "3"]
    list2 = file['newCol'].to_list()
    list2 = [list2[i] for i in range (len(list1)) if list1[i].split(":")[1][2] != "3"]
    text = '''
     <link rel="stylesheet" type = "text/css" href="{%static 'css/accueil.css'%}">
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'Conso'],
        '''
    for i in range(len(list1)-1) :
        text += "['"+list1[i]+"',"+str(list2[i])+"],\n"
    text += "['"+list1[len(list1)-1]+"',"+str(list2[len(list1)-1])+"]\n"
    text += '''
    ]);
        var options = {
          title: '',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart1'));

        chart.draw(data, options);
      }
    </script>
    '''
    time.sleep(5)
    os.remove("C:\data\coefficients-des-profils.csv")
    URL = "https://re.jrc.ec.europa.eu/pvg_tools/fr/#PVP"
    driver.get(URL)
    driver.find_element(By.ID, "tr_hordat").click() 
    driver.find_element(By.ID, "inputLat").click()
    driver.find_element(By.ID, "inputLat").send_keys(str(latitudeform))   
    driver.find_element(By.ID, "inputLon").click()
    driver.find_element(By.ID, "inputLon").send_keys(str(longitudeform))
    driver.find_element(By.ID, "btninputLatLon").click()
    Select(driver.find_element(By.ID,"select_database_hourly")).select_by_value(""+rayoform+"")
    Select(driver.find_element(By.ID,"hendyear")).select_by_value(""+datefinform1+"")
    Select(driver.find_element(By.ID,"hstartyear")).select_by_value(""+datedebutform1+"")
    driver.find_element(By.ID, "hourlyangle").click()
    driver.find_element(By.ID, "hourlyangle").send_keys(inclinaisonform)
    driver.find_element(By.ID, "hourlyaspect").click()
    driver.find_element(By.ID, "hourlyaspect").send_keys(azimutform)
    driver.find_element(By.ID, "hourlydownloadcsv").click()
    while(len(os.listdir('C:\data')) == 0 or (not os.path.exists('C:\data')) or os.listdir('C:\data')[0].endswith('.tmp')) :
        None
    filename = "C:\data\\" + os.listdir("C:\data")[0]
    file = pd.read_csv(filename,on_bad_lines='skip',skiprows=8,skipfooter=10)
    file = file.drop(columns=['G(i)','T2m','WS10m','Int'],axis = 1)
    file = file.sort_values('time')
    list1prod = file['time'].to_list()
    for i in range(len(list1prod)) :
        list1prod[i] = list1prod[i].split(":")[0]+":"+list1prod[i].split(":")[1][0]+list1prod[i].split(":")[1][1]+"00"
    list2prod = file['H_sun'].to_list()
    text += '''
    <link rel="stylesheet" type = "text/css" href="{%static 'css/accueil.css'%}">
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'Production'],
        '''
    for i in range(len(list1prod)-1) :
        text += "['"+list1prod[i]+"',"+str(list2prod[i])+"],\n"
    text += "['"+list1prod[len(list1prod)-1]+"',"+str(list2prod[len(list1prod)-1])+"]\n"
    text += '''
    ]);
        var options = {
          title: '',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart2'));

        chart.draw(data, options);
      }
    </script>
    '''
    
    with open("site_conso/templates/simulation1.txt", "r") as input:
        with open("site_conso/templates/simulation.html", "a") as output:
            output.truncate(0)
            for line in input:
                output.write(line)
            output.write(text)
    with open("site_conso/templates/simulation2.txt", "r") as input:
        with open("site_conso/templates/simulation.html", "a") as output:
            for line in input:
                output.write(line)
    os.remove(filename)
    time.sleep(5)
    driver.close()
    return render(request,'simulation.html')



def profil(request) :
    c = Compte.objects.get(connecte = True)
    
    return render(request,'profil.html',{"message1" : "Nom : "+c.nom, "message2" : "Prenom : "+ c.prenom,"message3" : "email : "+ c.email,"message4" : "Date d'anniversaire : "+ str(c.birthday)})


##https://re.jrc.ec.europa.eu/pvg_tools/fr/#PVP