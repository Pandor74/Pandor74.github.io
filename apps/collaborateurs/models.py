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
		print(path,' n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'existe')

	return os.path.join(path,'logo_projet'+'.'+right(filename,"."))

class Projet(models.Model):
	numero_teamber=models.CharField(max_length=255,verbose_name="Numéro Teamber ",primary_key=True,unique=True)
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
		return 'adresse'

	



class Propriete(models.Model):
	nb_logements=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre de logements ")
	nb_etages=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre d'étages ")
	surf_sol = models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface au sol (m²) ")
	surf_shon=models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface SHON (m²) ")
	date_fin=models.DateField(blank=True,null=True,verbose_name="Date de rendu ")

	projet=models.OneToOneField(Projet,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return 'je suis les propriétés du projet'



