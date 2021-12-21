from django.db import models

# Create your models here.
class Compte(models.Model):
    identifiant = models.IntegerField(unique = True,null =True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(null =True)
    birthday = models.DateField()
    password = models.CharField(max_length=32)
    connecte = models.BooleanField(null = True)
    email_verifie = models.BooleanField(default = False, null = True)

class Entite(models.Model):
    champ = models.CharField(max_length=255)

class PDL(models.Model):
    champ = models.CharField(max_length=255)