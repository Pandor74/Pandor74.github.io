from django import forms
from collaborateurs.models import Projet,Image
from django.forms import ModelForm,SelectDateWidget
from django.utils.translation import gettext_lazy as _

class ProjetForm(ModelForm):
	class Meta:
		model=Projet
		fields='__all__'
		localized_fields=('__all__')
		error_messages = {
			'nom': {'required': _(" "),},
			'date_creation': {'required': _(" "),},
			'date_exe': {'required': _(" "),},
			'annee_teamber': {'required': _(" "),},
			'numero_teamber': {'required': _(" "),},
			'nb_lots': {'required': _(" "),},
			'nb_etages': {'required': _(" "),},
			'surf_sol': {'required': _(" "),},
			'surf_shon': {'required': _(" "),},
			'photo': {'required': _(" "),},
		}
		widgets= {
			'date_creation': SelectDateWidget,
		}

class ImageForm(forms.Form):
	fichier=forms.ImageField()
	nom=forms.CharField()

