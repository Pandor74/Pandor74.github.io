from django import forms
from collaborateurs.models import Projet,Adresse,Personne,Propriete,Lot,DocumentLot,DomaineCompetence,Agence,Entreprise,SecteurGeographique
from collaborateurs.models import Echeance,AppelOffre,AppelOffreLot,AppelOffreGlobal
from django.forms import ModelForm,SelectDateWidget,Textarea,TextInput,FileInput,SelectMultiple
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator,FileExtensionValidator
import os
from django.core.exceptions import ValidationError
from os import path

from collaborateurs.fonction import right


from collaborateurs.models import LISTE_ACTIVITES,LISTE_CATEGORIE_FICHIER_LOT
from entreprises.models import LISTE_CATEGORIE_FICHIER_OFFRE






		
class ConnexionForm(forms.Form):
	username=forms.CharField(label="Nom d'utilisateur",max_length=30)
	password=forms.CharField(label="Mot de passe",widget=forms.PasswordInput)

