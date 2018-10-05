from django import forms
from collaborateurs.models import Projet,Adresse,Propriete,Lot,Document
from django.forms import ModelForm,SelectDateWidget,Textarea,TextInput,FileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

class ProjetForm(forms.ModelForm):
	class Meta:
		model=Projet
		exclude=['date_creation']
		localized_fields=('__all__')
		widgets= {
			'nom':TextInput(attrs={'size':40,'placeholder':'Nom du projet'}),
			'numero_teamber':TextInput(attrs={'size':40,'placeholder':'Numéro Teamber'}),
		}





class FiltreForm(forms.Form):
	FILTRES=(
		('-numero_teamber', 'Numero Teamber'),
		('nom', 'Nom de projet'),
		
	)
	
	filtre=forms.ChoiceField(choices=FILTRES,initial='-numero_teamber',label="Filtrer par ")
	search=forms.CharField(max_length=255,required=False,label="Recherche ")


class AdresseForm(forms.ModelForm):
	class Meta:
		model=Adresse
		exclude=['projet']
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



#inutilisé en raison de la compléxité de la gestion de plusieurs fichiers
class DocumentForm(forms.ModelForm):
	class Meta:
		model=Document
		exclude=['lot']



LISTE_CATEGORIE_FICHIER=(
		('DPGF','DPGF'),
		('CCTP','CCTP'),
		('PLAN','Plan'),
		('DIAG','Diagnostic'),
		('AUTRE','Autre'),
	)

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
	

	c1=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c2=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c3=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c4=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c5=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c6=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c7=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c8=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	c9=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER,initial="AUTRE",required=False)
	