from django.db import models
from django.utils import timezone
import datetime
from django import forms

# Create your models here.
class Adresse(models.Model):
	adresse1=models.CharField(default="NR",max_length=255,verbose_name="Adresse N°1 ")
	adresse2=models.CharField(default="NR",max_length=255,verbose_name="Adresse N°2 ")
	code_postal=models.CharField(default="NR",max_length=255,verbose_name="Code Postal ")
	ville=models.CharField(default="NR",max_length=255,verbose_name="Ville ")
	pays=models.CharField(default="France",max_length=255,verbose_name="Pays ")

	def __str__(self):
		return self.adresse1 + '-' + self.adresse2 + '-' + self.code_postal +'-' + self.ville + '-' + self.pays



class Projet(models.Model):
	nom=models.CharField(max_length=255,verbose_name="Nom du projet * ")
	date_creation = models.DateField(default=datetime.date.today,verbose_name="Date de création * ")
	date_exe=models.DateField(default=datetime.date.today,blank=True,null=True,verbose_name="Date de démarrage des travaux (facultatif) ")
	annee_teamber = models.IntegerField(verbose_name="Année Teamber * ")
	numero_teamber = models.IntegerField(verbose_name="Numéro Teamber * ")
	numero_identifiant=models.CharField(max_length=255,blank=True,null=True,verbose_name="Identifiant Teamber ")
	nb_lots=models.IntegerField(default=0,verbose_name="Nombre de lots (facultatif) ")
	nb_etages=models.IntegerField(default=0,verbose_name="Nombre d'étages (facultatif) ")
	surf_sol = models.IntegerField(default=0,verbose_name="Surface au sol (facultatif) ")
	surf_shon=models.IntegerField(default=0,verbose_name="Surface SHON (facultatif) ")
	photo=models.ImageField(upload_to="images/",default="images/logo.jpg",blank=True,null=True,verbose_name="Logo du projet  (facultatif) ")
	adresse=models.OneToOneField(Adresse,on_delete=models.CASCADE,null=True)


	class Meta:
		verbose_name="Projet"
		verbose_name_plural="Projets"
		ordering =['-annee_teamber','-numero_teamber']

	def __str__(self):
		return self.nom

	def save(self,*args,**kwargs):
		self.numero_identifiant=str(self.annee_teamber)+'-'+str(self.numero_teamber)
		super().save(*args,**kwargs)










