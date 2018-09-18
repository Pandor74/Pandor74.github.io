from django import forms
from collaborateurs.models import Projet,Image
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


class ImageForm(forms.Form):
	fichier=forms.ImageField()
	nom=forms.CharField()



class FiltreForm(forms.Form):
	FILTRES=(
		('numero', 'par numero'),
		('nom', 'par nom'),
		
	)
	
	filtre=forms.ChoiceField(choices=FILTRES)


