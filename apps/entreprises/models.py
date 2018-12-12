from django.db import models
import os
from django.conf import settings

from storage import OverwriteStorage
from collaborateurs.models import Lot,Agence,Projet,AppelOffre,AppelOffreLot,Personne
from collaborateurs.fonction import right,right_path




LISTE_STATUT_OFFRE =(
	('Non commencé','Non commencé'),
	('En cours','En cours'),
	('Terminé','Terminé'),
	)

# Create your models here.

class Offre(models.Model):

	lot=models.ForeignKey(Lot,on_delete=models.CASCADE,blank=True)
	personne=models.ForeignKey(Personne,on_delete=models.PROTECT,blank=True,null=True)
	appel_lot=models.ForeignKey(AppelOffreLot,on_delete=models.PROTECT,blank=True)
	statut=models.CharField(max_length=255,choices=LISTE_STATUT_OFFRE,default="Non commencé",blank=True,verbose_name="Statut de l'offre")



	def __str__(self):
		return 'Offre du lot ' + self.lot.short_name + ' créé par ' 



#défini le chemin d'enregistrement des fichiers des lots et créé le chemin si besoin dans le dossier projets
def fichier_offre_path(instance,filename):
	path=os.path.join(\
		settings.BASE_DIR,'media','fichiers','projets',\
		str(instance.offre.lot.projet.numero_teamber)+'-'+str(instance.offre.lot.projet.nom),\
		str(instance.offre.lot.nom),'AO-'+str(instance.offre.appel_lot.AO.numero),\
		str(instance.offre.personne.agence.entreprise.nom_ent)+'-'+str(instance.offre.personne.agence.nom))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)




#définit la liste des types de fichiers d'une offre DPGF, CTTP, autres .....
LISTE_CATEGORIE_FICHIER_OFFRE=(
		('DPGF','DPGF'),
		('CCTP','CCTP'),
		('AE','Acte d\'engagement'),
		('AUTRE','Autre'),
	)


class DocumentOffreLot(models.Model):
	fichier=models.FileField(upload_to=fichier_offre_path,blank=True,null=True,verbose_name="Document de l'offre : ",storage=OverwriteStorage())
	categorie=models.CharField(max_length=255,choices=LISTE_CATEGORIE_FICHIER_OFFRE,default="AUTRE",null=True,blank=True,verbose_name="Catégorie de document")

	offre=models.ForeignKey(Offre,on_delete=models.CASCADE,blank=True,related_name="documents")

	def nom(self):
		nom=right_path(self.fichier.path,"\\")
		return nom

	def taille(self):
		mem=self.fichier.size/1024
		mem=round(mem)

		return str(mem) + ' Mo'

	def get_extension(self):
		nom=self.nom()
		return right(nom,'.')


	def __str__(self):
		return os.path.basename(self.fichier.name)


