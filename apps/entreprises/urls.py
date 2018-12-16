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
from django.urls import path,include
from entreprises import views
from django.conf.urls import url

urlpatterns = [
	path('',views.home,name='ent_accueil'),

	#projets
    url(r'^projets$',views.Liste_Projet,name="ent_lister_projets"),
    url(r'^projet/(?P<pk>.{1,9})$',views.Afficher_Projet,name="ent_voir_projet"),
    url(r'^projet/(?P<pk>.{1,9})/lots$',views.Liste_Lot,name="ent_lister_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})$',views.Afficher_Lot,name="ent_voir_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/lot/(?P<pklot>\d{1,3})/telecharger-tout$',views.Get_Zipped_Files,name="ent_download_archive"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/fichier/(?P<iddoc>\d{1,3})-(?P<nom>.+)$',views.Voir_Fichier_PDF_Lot,name="ent_voir_fichier"),

]