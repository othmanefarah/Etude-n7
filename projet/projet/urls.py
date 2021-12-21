"""projet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from site_conso import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Accueil', views.accueil, name = "accueil"),
    path('Accueil0',views.NewAccueil,name ="NewAccueil"),
    path('Inscription', views.inscription),
    path('Profil', views.profil),
    path('Connexion', views.connexion),
    path('Inscription0', views.newUser),
    path('Connexion0', views.login),
    path('Activate',views.activation),
]

