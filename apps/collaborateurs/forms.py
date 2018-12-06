from django import forms
from collaborateurs.models import Projet,Adresse,Personne,Propriete,Lot,DocumentLot,DomaineCompetence,Agence,Entreprise,SecteurGeographique
from django.forms import ModelForm,SelectDateWidget,Textarea,TextInput,FileInput,SelectMultiple
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator

from collaborateurs.models import LISTE_ACTIVITES,LISTE_CATEGORIE_FICHIER_LOT

class ProjetForm(forms.ModelForm):
	class Meta:
		model=Projet
		exclude=['date_creation']
		localized_fields=('__all__')
		widgets= {
			'nom':TextInput(attrs={'size':40,'placeholder':'Nom du projet'}),
			'numero_teamber':TextInput(attrs={'size':40,'placeholder':'Numéro Teamber'}),
		}





class FiltreFormProjet(forms.Form):
	FILTRES_PROJET=(
		('-numero_teamber', 'Numero Teamber'),
		('nom', 'Nom de projet'),
		
	)
	
	filtre=forms.ChoiceField(choices=FILTRES_PROJET,initial='-numero_teamber',label="Trier par ")
	search=forms.CharField(max_length=255,required=False,label="Recherche ")



class FiltreFormContact(forms.Form):
	FILTRES_CONTACT=(
		('tous', 'Tous'),
		('entreprise', 'Entreprises'),
		('agence', 'Agences'),
		('personne', 'Personnes'),
	)
	
	filtre=forms.ChoiceField(choices=FILTRES_CONTACT,initial='tous',label="Afficher ",widget=forms.Select(attrs={'title':'Permet de filtrer par catégorie de contact'}))
	search=forms.CharField(max_length=255,required=False,label="Recherche ",widget=forms.TextInput(attrs={'title':'Recherche dans le nom, le prénom ou le numéro SIREN/SIRET le cas échéant'}))



class AdresseForm(forms.ModelForm):
	class Meta:
		model=Adresse
		exclude=['projet','agence']
		widgets= {
			'adresse1':TextInput(attrs={'size':40,'placeholder':'N° et nom de rue'}),
			'adresse2':TextInput(attrs={'size':40,'placeholder':'Batiment, étage ...'}),
			'code_postal':TextInput(attrs={'size':40,'placeholder':'Code Postal'}),
			'ville':TextInput(attrs={'size':40,'placeholder':'Ville'}),
			'pays':TextInput(attrs={'size':40,'placeholder':'Pays'}),
		}
		

class ProprietesForm(forms.ModelForm):
	class Meta:
		model=Propriete
		exclude=['projet']
		widgets= {
			'date_fin': SelectDateWidget(),
			}


class LotForm(forms.ModelForm):
	class Meta:
		model=Lot
		exclude=['projet','publier']
		widgets= {
			'nom':TextInput(attrs={'size':40,'placeholder':'Nom complet du lot'}),
			'short_name':TextInput(attrs={'size':40,'placeholder':'Nom court du lot (max 10 char)'}),
			'numero':TextInput(attrs={'size':40,'placeholder':'Numéro du lot'}),
		}


#inutilisé en raison de la compléxité de la gestion de plusieurs fichiers
class DocumentLotForm(forms.ModelForm):
	class Meta:
		model=DocumentLot
		exclude=['lot']



class FichiersForm(forms.Form):
	fDPGF=forms.FileField(required=False,label="Fichier DPGF (Excel) :")
	fCCTP=forms.FileField(required=False,label="Fichier CCTP (Word/PDF) :")
	f1=forms.FileField(required=False,label="Fichier annexe N°1 :")
	f2=forms.FileField(required=False,label="Fichier annexe N°2:")
	f3=forms.FileField(required=False,label="Fichier annexe N°3:")
	f4=forms.FileField(required=False,label="Fichier annexe N°4:")
	f5=forms.FileField(required=False,label="Fichier annexe N°5:")
	f6=forms.FileField(required=False,label="Fichier annexe N°6:")
	f7=forms.FileField(required=False,label="Fichier annexe N°7:")
	f8=forms.FileField(required=False,label="Fichier annexe N°8:")
	f9=forms.FileField(required=False,label="Fichier annexe N°9:")
	

	c1=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c2=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c3=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c4=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c5=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c6=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c7=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c8=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)
	c9=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_LOT,initial="AUTRE",required=False)




class CompetenceForm(forms.Form):
	competences=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=LISTE_ACTIVITES,required=True)


class AgenceForm(forms.ModelForm):
	class Meta:
		model=Agence
		exclude=['entreprise','lots','date_inscription_agence']
		widgets = {
			'date_creation_agence' : SelectDateWidget(years=range(timezone.now().year,1900,-1)),
			'competences_agence': forms.CheckboxSelectMultiple(),
		}



class EntrepriseForm(forms.ModelForm):
	class Meta:
		model=Entreprise
		exclude=['date_inscription_ent']
		widgets = {
			'date_creation_ent' : SelectDateWidget(years=range(timezone.now().year,1900,-1)),
		}


class PersonneForm(forms.ModelForm):
	class Meta:
		model=Personne
		exclude=['date_inscription_personne','agence']


class SiretForm(forms.Form):
	SIRET_regex=RegexValidator(regex=r'^(?P<siret>\d{14})$',message="Le numéro SIRET doit être composé de 13 chiffres")
	num_SIRET=forms.CharField(validators=[SIRET_regex],max_length=14,label="N°SIRET de l'agence")


