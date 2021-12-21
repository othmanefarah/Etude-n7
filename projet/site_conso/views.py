from typing import Generic
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Compte
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.urls import reverse
import random
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


def profil(request) :
    c = Compte.objects.get(connecte = True)
    
    return render(request,'profil.html',{"message1" : "Nom : "+c.nom, "message2" : "Prenom : "+ c.prenom,"message3" : "email : "+ c.email,"message4" : "Date d'anniversaire : "+ str(c.birthday)})


