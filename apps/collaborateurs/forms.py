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
			'date_fin': SelectDateWidget(years=range(timezone.now().year,2100,+1)),
			}
		

	def clean_date_fin(self):
		date = self.cleaned_data['date_fin']
		if date:
			if date <= datetime.date.today():
				raise forms.ValidationError("La date ne peut pas être dans le passé !")
			return date



class LotForm(forms.ModelForm):
	class Meta:
		model=Lot
		exclude=['projet','publier']
		widgets= {
			'nom':TextInput(attrs={'size':40,'placeholder':'Nom complet du lot'}),
			'short_name':TextInput(attrs={'size':40,'placeholder':'Nom court du lot (max 10 char)'}),
			'numero':TextInput(attrs={'size':40,'placeholder':'Numéro du lot'}),
			'activites':forms.CheckboxSelectMultiple(),
		}



#inutilisé en raison de la compléxité de la gestion de plusieurs fichiers
class DocumentLotForm(forms.ModelForm):
	class Meta:
		model=DocumentLot
		exclude=['lot']






class FichiersForm(forms.Form):
	f1=forms.FileField(required=False,label="Fichier annexe N°1:")
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

	def __init__(self,docs,*args,**kwargs):
		super(FichiersForm,self).__init__(*args,**kwargs)
		nombre=docs.count()
		print('nombre doc init :',nombre)

		if nombre == 1: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
		elif nombre == 2: 
				print(docs[0].fichier)
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
		elif nombre == 3: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
		elif nombre == 4: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
		elif nombre == 5: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
				self.fields['f5'].initial=docs[4].fichier
				self.fields['c5'].initial=docs[4].categorie
		elif nombre == 6: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
				self.fields['f5'].initial=docs[4].fichier
				self.fields['c5'].initial=docs[4].categorie
				self.fields['f6'].initial=docs[5].fichier
				self.fields['c6'].initial=docs[5].categorie
		elif nombre == 7: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
				self.fields['f5'].initial=docs[4].fichier
				self.fields['c5'].initial=docs[4].categorie
				self.fields['f6'].initial=docs[5].fichier
				self.fields['c6'].initial=docs[5].categorie
				self.fields['f7'].initial=docs[6].fichier
				self.fields['c7'].initial=docs[6].categorie

		elif nombre == 8: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
				self.fields['f5'].initial=docs[4].fichier
				self.fields['c5'].initial=docs[4].categorie
				self.fields['f6'].initial=docs[5].fichier
				self.fields['c6'].initial=docs[5].categorie
				self.fields['f7'].initial=docs[6].fichier
				self.fields['c7'].initial=docs[6].categorie
				self.fields['f8'].initial=docs[7].fichier
				self.fields['c8'].initial=docs[7].categorie
		elif nombre == 9: 
				self.fields['f1'].initial=docs[0].fichier
				self.fields['c1'].initial=docs[0].categorie
				self.fields['f2'].initial=docs[1].fichier
				self.fields['c2'].initial=docs[1].categorie
				self.fields['f3'].initial=docs[2].fichier
				self.fields['c3'].initial=docs[2].categorie
				self.fields['f4'].initial=docs[3].fichier
				self.fields['c4'].initial=docs[3].categorie
				self.fields['f5'].initial=docs[4].fichier
				self.fields['c5'].initial=docs[4].categorie
				self.fields['f6'].initial=docs[5].fichier
				self.fields['c6'].initial=docs[5].categorie
				self.fields['f7'].initial=docs[6].fichier
				self.fields['c7'].initial=docs[6].categorie
				self.fields['f8'].initial=docs[7].fichier
				self.fields['c8'].initial=docs[7].categorie
				self.fields['f9'].initial=docs[8].fichier
				self.fields['c9'].initial=docs[8].categorie
				

		





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


class EcheanceForm(forms.ModelForm):
	class Meta:
		model=Echeance
		exclude=['appel','appelLot','projet','appelGlobal']
		widgets ={
			'date':SelectDateWidget(years=range(timezone.now().year,2100,+1))
		}

	def clean_date(self):
		date = self.cleaned_data['date']
		if date <= datetime.date.today():
			raise forms.ValidationError("La date ne peut pas être dans le passé !")
		return date



class AppelOffreForm(forms.ModelForm):
	class Meta:
		model=AppelOffre
		exclude=['projet']
		widgets ={
			'lots':forms.CheckboxSelectMultiple(),
		}

	def __init__(self,projet,*args,**kwargs):
		super(AppelOffreForm,self).__init__(*args,**kwargs)
		self.fields['lots'].queryset=Lot.objects.filter(projet=projet)


		

class AppelOffreLotForm(forms.ModelForm):
	class Meta:
		model=AppelOffreLot
		exclude=['projet','AO','lot','date_de_creation']
		widgets ={
			'AO_agences':forms.CheckboxSelectMultiple(),
			'AO_personnes':forms.CheckboxSelectMultiple(),
			'date_lancement':SelectDateWidget(years=range(timezone.now().year,2100,+1))
		}

	def __init__(self,agences,personnes,*args,**kwargs):
		super(AppelOffreLotForm,self).__init__(*args,**kwargs)
		self.fields['AO_agences'].queryset=agences
		self.fields['AO_personnes'].queryset=personnes

	def clean_date_lancement(self):
		date = self.cleaned_data['date_lancement']
		if date:
			if date < datetime.date.today():
				raise forms.ValidationError("La date ne peut pas être dans le passé !")
			return date


class AppelOffreGlobalForm(forms.ModelForm):
	class Meta:
		model=AppelOffreGlobal
		fields='__all__'



class FiltreFormAgenceAO(forms.Form):
	competences=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'title':'Selectionner les activités recherchées'}),choices=LISTE_ACTIVITES,required=False)
	search=forms.CharField(max_length=255,required=False,label="Recherche ")


class FiltreFormPersonneAO(forms.Form):
	competences=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=LISTE_ACTIVITES)
