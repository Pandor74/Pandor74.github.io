from django.db import models
from django.utils import timezone
import datetime
from django import forms

# Create your models here.
class Adresse(models.Model):
	adresse1=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Adresse N°1 ")
	adresse2=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Adresse N°2 ")
	code_postal=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Code Postal ")
	ville=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Ville ")
	pays=models.CharField(default="France",null=True,blank=True,max_length=255,verbose_name="Pays ")

	def __str__(self):
		return self.adresse1 + '-' + self.adresse2 + '-' + self.code_postal +'-' + self.ville + '-' + self.pays


class PropProjet(models.Model):
	nb_logements=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre de logements ")
	nb_etages=models.IntegerField(default=0,null=True,blank=True,verbose_name="Nombre d'étages ")
	surf_sol = models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface au sol (m²) ")
	surf_shon=models.IntegerField(default=0,null=True,blank=True,verbose_name="Surface SHON (m²) ")
	date_fin=models.DateField(blank=True,null=True,verbose_name="Date de rendu ")

	def __str__(self):
		return 'je suis les propriétés du projet'



class Projet(models.Model):
	numero_teamber=models.CharField(max_length=255,verbose_name="Numéro Teamber ",primary_key=True,unique=True)
	nom=models.CharField(max_length=255,verbose_name="Nom du projet ")
	agence=models.CharField(max_length=20,default="Annecy",choices=(('Annecy','Annecy'),('Lyon','Lyon')),null=True,blank=True,verbose_name="Agence interne")
	photo=models.ImageField(upload_to="images/",default="images/logo.jpg",blank=True,null=True,verbose_name="Photo du projet (facultatif) ")

	
	date_creation = models.DateField(default=datetime.date.today,verbose_name="Date de création ")

	adresse=models.OneToOneField(Adresse,on_delete=models.CASCADE,null=True)
	proprietes=models.OneToOneField(PropProjet,on_delete=models.CASCADE,null=True)


	class Meta:
		verbose_name="Projet"
		verbose_name_plural="Projets"
		ordering =['-numero_teamber']

	def __str__(self):
		return self.nom

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)










