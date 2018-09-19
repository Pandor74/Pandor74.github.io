from django import forms
from collaborateurs.models import Projet,Adresse
from django.forms import ModelForm,SelectDateWidget
from django.utils.translation import gettext_lazy as _

class ProjetForm(ModelForm):
	class Meta:
		model=Projet
		exclude=['date_creation']
		localized_fields=('__all__')
		widgets= {
			'date_exe': SelectDateWidget,
		}
		initial={
			'nom':'nom du projet',
		}




class FiltreForm(forms.Form):
	FILTRES=(
		('-numero_identifiant', 'par numero'),
		('nom', 'par nom'),
		
	)
	
	filtre=forms.ChoiceField(choices=FILTRES,initial='numero',label="Filtrer par ")
	search=forms.CharField(max_length=255,required=False,label="Recherche ")





