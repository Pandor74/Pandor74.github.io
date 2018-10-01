from django import forms
from collaborateurs.models import Projet,Adresse,Propriete
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
			'adresse1':TextInput(attrs={'size':40}),
			'adresse2':TextInput(attrs={'size':40}),
			'code_postal':TextInput(attrs={'size':40}),
			'ville':TextInput(attrs={'size':40}),
			'pays':TextInput(attrs={'size':40}),
		}
		

class ProprietesForm(forms.ModelForm):
	class Meta:
		model=Propriete
		exclude=['projet']
		widgets= {
			'date_fin': SelectDateWidget(),
			}


