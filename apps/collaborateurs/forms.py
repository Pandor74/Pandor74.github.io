from django import forms
from collaborateurs.models import Projet,Adresse
from django.forms import ModelForm,SelectDateWidget,Textarea,TextInput
from django.utils.translation import gettext_lazy as _

class ProjetForm(forms.ModelForm):
	class Meta:
		model=Projet
		exclude=['date_creation','adresse','proprietes']
		localized_fields=('__all__')
		widgets= {
			'date_exe': SelectDateWidget,
			'nom':TextInput(attrs={'size':40,'placeholder':'Numéro Teamber'}),
			'numero_teamber':TextInput(attrs={'size':40}),
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
		fields='__all__'
		widgets= {
			'adresse1':TextInput(attrs={'size':40}),
			'adresse2':TextInput(attrs={'size':40}),
			'code_postal':TextInput(attrs={'size':40}),
			'ville':TextInput(attrs={'size':40}),
			'pays':TextInput(attrs={'size':40}),
		}

		


