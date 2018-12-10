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
	
    url(r'^projets$',views.ListeProjets.as_view(),name="projets_liste"),
    url(r'^projets/nouveau-projet$',views.New_Projet,name="nouveau_projet"),
    url(r'^projet/modifier/(?P<pk>.+)$',views.Modifier_Projet,name="modifier_projet"),
    url(r'^projet/(?P<pk>.{1,9})$',views.Afficher_Projet,name="voir_projet"),
    url(r'^projet/(?P<pk>.{1,9})/nouveau-lot$',views.New_Lot,name="nouveau_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lots$',views.Liste_Lot,name="lister_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})$',views.Afficher_Lot,name="voir_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/modifier-paramètres$',views.Modifier_Lot,name="modifier_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/modifier-fichiers$',views.Modifier_Fichiers_Lot,name="modifier_fichiers_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/fichier/(?P<iddoc>\d{1,3})-(?P<nom>.+)$',views.Voir_Fichier_PDF_Lot,name="voir_fichier"),
    url(r'^projet/(?P<pk>.{1,9})/nouveau-ao$',views.New_AO,name="nouveau_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})$',views.Afficher_AO,name="voir_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/modifier$',views.Modifier_AO,name="modifier_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/gerer$',views.Gerer_AO_Lot,name="gerer_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/nouveau-ao-lot$',views.New_AO_Lot,name="nouveau_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/ao-lot-(?P<pkAOlot>.{1,9})$',views.Afficher_AO_Lot,name="voir_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/ao-lot-(?P<pkAOlot>.{1,9})/selectionner-contacts$',views.Selectionner_Contact_AO_Lot,name="select_contact_ao_lot"),

    url(r'^contacts/$',views.Liste_Contact,name="contacts_liste"),
    url(r'^contacts/nouvelle_entreprise/$',views.New_Entreprise_Et_Agence,name="nouvelle_entreprise"),
    url(r'^contacts/nouvelle_personne/$',views.New_Personne,name="nouvelle_personne"),
    url(r'^contacts/nouvelle_personne/nouvelle_entreprise/(?P<siret>\d{14})-(?P<pk>.{1,9})$',views.Associer_New_Entreprise_Et_Agence,name="associer_nouvelle_entreprise_et_agence"),
    url(r'^contacts/nouvelle_personne/nouvelle_agence/(?P<siret>\d{14})-(?P<pk>.{1,9})$',views.Associer_New_Agence,name="associer_nouvelle_agence"),
    url(r'^contacts/entreprises/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Afficher_Entreprise,name="voir_entreprise"),
    url(r'^contacts/entreprises/modifier/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Modifier_Entreprise,name="modifier_entreprise"),
    url(r'^contacts/entreprises/nouvelle_agence/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Add_Agence,name="ajouter_agence"),
    url(r'^contacts/entreprises/nouvelle_personne/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Add_Personne,name="ajouter_personne"),
    url(r'^contacts/agences/(?P<pk>.{1,9})-(?P<nom>.+)$',views.Afficher_Agence,name="voir_agence"),
    url(r'^contacts/agences/modifier/(?P<pk>.{1,9})-(?P<nom>.+)$',views.Modifier_Agence,name="modifier_agence"),
    url(r'^contacts/personnes/(?P<pk>.{1,9})-(?P<nom>.+)-(?P<prenom>.+)$',views.Afficher_Personne,name="voir_personne"),
    url(r'^contacts/personnes/modifier/(?P<pk>.{1,9})-(?P<nom>.+)-(?P<prenom>.+)$',views.Modifier_Personne,name="modifier_personne"),


]