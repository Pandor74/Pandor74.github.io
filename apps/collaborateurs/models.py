from django.db import models
from django.utils import timezone
import datetime
from django import forms
from storage import OverwriteStorage
import os
from django.conf import settings







def right(name,char):
	left,right=name.split(char)
	return right


def image_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','images',str(instance.numero_teamber))

	if not os.path.isdir(path):
		print(path,' chemin image n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin image existe')

	return os.path.join(path,'logo_projet'+'.'+right(filename,"."))




class Projet(models.Model):
	numero_teamber=models.CharField(max_length=255,verbose_name="Numéro Teamber (unique) ",primary_key=True,unique=True)
	nom=models.CharField(max_length=255,verbose_name="Nom du projet ")
	agence=models.CharField(max_length=20,default="Annecy",choices=(('Annecy','Annecy'),('Lyon','Lyon')),null=True,blank=True,verbose_name="Agence interne")
	photo=models.ImageField(upload_to=image_path,blank=True,null=True,verbose_name="Photo du projet (facultatif) ",storage=OverwriteStorage())
	
	
	date_creation = models.DateField(default=datetime.date.today,verbose_name="Date de création ")

	
	class Meta:
		verbose_name="Projet"
		verbose_name_plural="Projets"
		ordering =['-numero_teamber']

	def __str__(self):
		return self.nom

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

	def image_path(instance,filename):
		return os.path.join('images/',str(instance.numero_teamber),'/')






# Create your models here.
class Adresse(models.Model):
	adresse1=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Adresse N°1 ")
	adresse2=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Adresse N°2 ")
	code_postal=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Code Postal ")
	ville=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Ville ")
	pays=models.CharField(default="France",null=True,blank=True,max_length=255,verbose_name="Pays ")

	projet=models.OneToOneField(Projet,on_delete=models.CASCADE,null=True)
	

	def __str__(self):
		return 'adresse de ' + self.projet.numero_teamber

	
LISTE_ARCHITECTURE =(
		('basique','Basique'),
		('moyenne','Moyenne'),
		('complexe','Complexe'),
	)

LISTE_SECTEUR=(
		('copro','Copropriété'),
		('tertiaire','Tertiaire'),
		('social','Social'),
		('individuel','Individuel')
	)

LISTE_TRAVAUX=(
		('reno','Rénovation'),
		('sinistre','Sinistre'),
		('neuf','Neuf'),
	)

LISTE_CONSULTATION=(
		('lot','Marché par lot'),
		('global','Marché global'),
	)

class Propriete(models.Model):
	nb_logements=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre de logements ")
	nb_etages=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre d'étages ")
	surf_sol = models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface au sol (m²) ")
	surf_shon=models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface SHON (m²) ")
	date_fin=models.DateField(blank=True,null=True,verbose_name="Date de rendu ")
	architecture=models.CharField(max_length=255,choices=LISTE_ARCHITECTURE,null=True,blank=True,verbose_name="Type d'architecture ")
	secteur=models.CharField(max_length=255,choices=LISTE_SECTEUR,null=True,blank=True,verbose_name="Catégorie de clientèle ")
	travaux=models.CharField(max_length=255,choices=LISTE_TRAVAUX,null=True,blank=True,verbose_name="Type de travaux")
	consultation=models.CharField(max_length=255,choices=LISTE_CONSULTATION,null=True,blank=True,verbose_name="Mode de consultation")

	projet=models.OneToOneField(Projet,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return 'propriétés de ' + self.projet.numero_teamber



LISTE_ACTIVITES =(
		('Faca','Façades'),
		('Elec','Electricité'),
	)

LISTE_SUFFIXE=(
		('','Suffixe'),
		('A','A'),
		('B','B'),
		('C','C'),
		('bis','Bis'),
		('ter','Ter'),
	)



class Lot(models.Model):
	numero=models.IntegerField(default=0,verbose_name="Numéro du lot ")
	suffixe=models.CharField(max_length=5,default='',blank=True,choices=LISTE_SUFFIXE,verbose_name="Suffixe")
	description=models.TextField(null=True,blank=True,verbose_name="Description succincte ",help_text="Décrivez de manière succincte les éléments constitutifs du travail à faire")
	short_name=models.CharField(max_length=10,null=True,verbose_name="Nom court pour identifier le lot facilement",help_text="Sera utilisé dans la barre de navigation")
	nom=models.CharField(max_length=255,null=True,verbose_name="Nom du lot ")

	publier=models.BooleanField(default=False)

	projet=models.ForeignKey(Projet,on_delete=models.CASCADE)
	activites=models.CharField(max_length=255,choices=LISTE_ACTIVITES,verbose_name="Types d'activités relative au lot")

	class Meta:
		ordering=['numero','suffixe']


	def __str__(self):
		return 'N° ' + str(self.numero) + ' ' + self.suffixe + ' - ' + self.short_name

	def decris_toi(self):
		return ' N°' + str(self.numero) + ' ' + self.suffixe + ' : ' + self.short_name + ' - ' + self.nom



#défini le chemin d'enregistrement des fichiers des lots
def fichier_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers',str(instance.lot.projet.numero_teamber),str(instance.lot.nom))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)



LISTE_CATEGORIE_FICHIER=(
		('DPGF','DPGF'),
		('CCTP','CCTP'),
		('PLAN','Plan'),
		('DIAG','Diagnostic'),
		('AUTRE','Autre'),
	)

class Document(models.Model):
	fichier=models.FileField(upload_to=fichier_path,blank=True,null=True,verbose_name="Document du projet : ",storage=OverwriteStorage())
	categorie=models.CharField(max_length=255,choices=LISTE_CATEGORIE_FICHIER,default="AUTRE",null=True,blank=True,verbose_name="Catégorie de document")

	lot=models.ForeignKey(Lot,on_delete=models.CASCADE)

	def __str__(self):
		return self.fichier.name