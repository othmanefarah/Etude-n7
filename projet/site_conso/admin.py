from django.contrib import admin
from .models import Compte, Entite, PDL, Simulations
# Register your models here.

admin.site.register(Compte)
admin.site.register(Entite)
admin.site.register(PDL)
admin.site.register(Simulations)