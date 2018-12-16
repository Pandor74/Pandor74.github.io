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





class FichiersFormOffre(forms.Form):
	f1=forms.FileField(required=False,label="Fichier annexe N°1:")
	f2=forms.FileField(required=False,label="Fichier annexe N°2:")
	f3=forms.FileField(required=False,label="Fichier annexe N°3:")
	f4=forms.FileField(required=False,label="Fichier annexe N°4:")
	f5=forms.FileField(required=False,label="Fichier annexe N°5:")
	f6=forms.FileField(required=False,label="Fichier annexe N°6:")
	f7=forms.FileField(required=False,label="Fichier annexe N°7:")
	f8=forms.FileField(required=False,label="Fichier annexe N°8:")
	f9=forms.FileField(required=False,label="Fichier annexe N°9:")
	

	c1=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c2=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c3=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c4=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c5=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c6=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c7=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c8=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)
	c9=forms.ChoiceField(choices=LISTE_CATEGORIE_FICHIER_OFFRE,initial="AUTRE",required=False)

	def __init__(self,docs,*args,**kwargs):
		super(FichiersFormOffre,self).__init__(*args,**kwargs)
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
				

		


