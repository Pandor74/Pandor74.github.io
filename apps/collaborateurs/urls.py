"""plateforme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include,re_path
from collaborateurs import views
from django.views.generic import ListView
from .models import Projet
from django.conf.urls import url

urlpatterns = [
	path('',views.Home,name='accueil_col'),
	path('deconnexion',views.Deconnexion,name='deconnexion'),
	path('nouveau_projet',views.New_Projet,name="nouveau_projet"),
    url('projets/',views.ListeProjets.as_view(),name="projets_liste"),
    url(r'^projet/modifier/(?P<pk>.+)$',views.Modifier_Projet,name="modifier_projet"),
    url(r'^projet/(?P<pk>.{1,9})$',views.Afficher_Projet,name="voir_projet"),
    url(r'^projet/(?P<pk>.{1,9})/nouveau-lot$',views.New_Lot,name="nouveau_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lots$',views.Liste_Lot,name="lister_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<id>\d{1,3})$',views.Afficher_Lot,name="voir_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<id>\d{1,3})/fichier/(?P<iddoc>\d{1,3})-(?P<nom>.+)$',views.Voir_Fichier_PDF_Lot,name="voir_fichier"),
    url('contacts/',views.Liste_Contact,name="contacts_liste"),
    url('nouvelle_entreprise',views.New_Entreprise,name="nouveau_entreprise"),
    url(r'^entreprise/(?P<pk>\d+)$',views.Afficher_Entreprise,name="voir_entreprise"),


]