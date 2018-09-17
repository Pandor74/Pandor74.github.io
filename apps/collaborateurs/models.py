from django.db import models
from django.utils import timezone
import datetime
from django import forms

# Create your models here.

class Projet(models.Model):
	nom=models.CharField(max_length=255,verbose_name="Nom du projet * ")
	date_creation = models.DateField(default=datetime.date.today,verbose_name="Date de création * ")
	date_exe=models.DateField(default=None,blank=True,null=True,verbose_name="Date de démarrage des travaux (facultatif) ")
	annee_teamber = models.IntegerField(verbose_name="Année Teamber * ")
	numero_teamber = models.IntegerField(verbose_name="Numéro Teamber * ")
	nb_lots=models.IntegerField(default=0,verbose_name="Nombre de lots (facultatif) ")
	nb_etages=models.IntegerField(default=0,verbose_name="Nombre d'étages (facultatif) ")
	surf_sol = models.IntegerField(default=0,verbose_name="Surface au sol (facultatif) ")
	surf_shon=models.IntegerField(default=0,verbose_name="Surface SHON (facultatif) ")
	photo=models.ImageField(upload_to="images/",null=True,verbose_name="Logo du projet  (facultatif) ")




	class Meta:
		verbose_name="Projet"
		ordering =['-annee_teamber','numero_teamber']

	def __str__(self):

		return self.nom

class Image(models.Model):
	fichier=models.ImageField(upload_to="images/")
	nom=models.CharField(max_length=100)

	def __str__(self):
		return self.nom


