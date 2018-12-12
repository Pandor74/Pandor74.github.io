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
	path('',views.Home,name='col_accueil'),
	path('deconnexion',views.Deconnexion,name='col_deconnexion'),
	
    #projets
    url(r'^projets$',views.ListeProjets.as_view(),name="col_lister_projets"),
    url(r'^projets/nouveau-projet$',views.New_Projet,name="col_nouveau_projet"),
    url(r'^projet/modifier/(?P<pk>.+)$',views.Modifier_Projet,name="col_modifier_projet"),
    url(r'^projet/(?P<pk>.{1,9})$',views.Afficher_Projet,name="col_voir_projet"),
    url(r'^projet/(?P<pk>.{1,9})/nouveau-lot$',views.New_Lot,name="col_nouveau_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lots$',views.Liste_Lot,name="col_lister_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})$',views.Afficher_Lot,name="col_voir_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/modifier-paramètres$',views.Modifier_Lot,name="col_modifier_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/modifier-fichiers$',views.Modifier_Fichiers_Lot,name="col_modifier_fichiers_lot"),
    url(r'^projet/(?P<pk>.{1,9})/lot/(?P<pklot>\d{1,3})/fichier/(?P<iddoc>\d{1,3})-(?P<nom>.+)$',views.Voir_Fichier_PDF_Lot,name="col_voir_fichier"),
    
    #appels d'offres
    url(r'^projet/(?P<pkprojet>.{1,9})/AO$',views.Lister_AO,name="col_lister_ao"),
    url(r'^projet/(?P<pk>.{1,9})/nouveau-ao$',views.New_AO,name="col_nouveau_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})$',views.Afficher_AO,name="col_voir_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/modifier$',views.Modifier_AO,name="col_modifier_ao"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/gerer$',views.Gerer_AO_Lot,name="col_gerer_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/nouveau-ao-lot$',views.New_AO_Lot,name="col_nouveau_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/ao-lot-(?P<pkAOlot>.{1,9})$',views.Afficher_AO_Lot,name="col_voir_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/ao-lot-(?P<pkAOlot>.{1,9})/modifier$',views.Modifier_AO_Lot,name="col_modifier_ao_lot"),
    url(r'^projet/(?P<pkprojet>.{1,9})/ao/(?P<pkAO>.{1,9})/lot/(?P<pklot>.{1,9})/ao-lot-(?P<pkAOlot>.{1,9})/selectionner-contacts$',views.Selectionner_Contact_AO_Lot,name="col_select_contact_ao_lot"),

    #contacts
    url(r'^contacts/$',views.Liste_Contact,name="col_contacts_liste"),
    url(r'^contacts/nouvelle_entreprise/$',views.New_Entreprise_Et_Agence,name="col_nouvelle_entreprise"),
    url(r'^contacts/nouvelle_personne/$',views.New_Personne,name="col_nouvelle_personne"),
    url(r'^contacts/nouvelle_personne/nouvelle_entreprise/(?P<siret>\d{14})-(?P<pk>.{1,9})$',views.Associer_New_Entreprise_Et_Agence,name="col_associer_nouvelle_entreprise_et_agence"),
    url(r'^contacts/nouvelle_personne/nouvelle_agence/(?P<siret>\d{14})-(?P<pk>.{1,9})$',views.Associer_New_Agence,name="col_associer_nouvelle_agence"),
    url(r'^contacts/entreprises/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Afficher_Entreprise,name="col_voir_entreprise"),
    url(r'^contacts/entreprises/modifier/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Modifier_Entreprise,name="col_modifier_entreprise"),
    url(r'^contacts/entreprises/nouvelle_agence/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Add_Agence,name="col_ajouter_agence"),
    url(r'^contacts/entreprises/nouvelle_personne/(?P<pk>.{1,9})-(?P<nom>.+)/$',views.Add_Personne,name="col_ajouter_personne"),
    url(r'^contacts/agences/(?P<pk>.{1,9})-(?P<nom>.+)$',views.Afficher_Agence,name="col_voir_agence"),
    url(r'^contacts/agences/modifier/(?P<pk>.{1,9})-(?P<nom>.+)$',views.Modifier_Agence,name="col_modifier_agence"),
    url(r'^contacts/personnes/(?P<pk>.{1,9})-(?P<nom>.+)-(?P<prenom>.+)$',views.Afficher_Personne,name="col_voir_personne"),
    url(r'^contacts/personnes/modifier/(?P<pk>.{1,9})-(?P<nom>.+)-(?P<prenom>.+)$',views.Modifier_Personne,name="col_modifier_personne"),
    url(r'^contacts/personnes/corriger/(?P<pk>.{1,9})$',views.Corriger_Erreur_Personne,name="col_corriger_erreur_personne"),

]