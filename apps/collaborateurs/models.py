from django.db import models
from django.utils import timezone
import datetime
from django import forms
from storage import OverwriteStorage
import os
from django.conf import settings
from django.core.validators import RegexValidator,MaxValueValidator
from collaborateurs.fonction import right,right_path







#définit et créé si besoin le chemin d'enregistrement des fichiers de type image pour le logo du projet
def image_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers','projets',str(instance.numero_teamber)+'-'+instance.nom)

	if not os.path.isdir(path):
		print(path,' chemin image n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin image existe')

	return os.path.join(path,'logo_projet'+'.'+right(filename,"."))



#défini le modèle Projet
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
		return str(self.numero_teamber) + '-' + self.nom

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

	def image_path(instance,filename):
		return os.path.join('images/',str(instance.numero_teamber),'/')





#comporte la liste des types d'architecture
LISTE_ARCHITECTURE =(
		('Basique','Basique'),
		('Moyenne','Moyenne'),
		('Complexe','Complexe'),
	)

#comporte la liste des secteurs d'activités
LISTE_SECTEUR=(
		('Copropriété','Copropriété'),
		('Tertiaire','Tertiaire'),
		('Social','Social'),
		('Individuel','Individuel')
	)

#définit la liste des catégories de travaux
LISTE_TRAVAUX=(
		('Rénovation','Rénovation'),
		('Sinistre','Sinistre'),
		('Neuf','Neuf'),
	)
#définit la liste des types de consultations
LISTE_CONSULTATION=(
		('lot','Marché par lot'),
		('global','Marché global'),
	)

#définit le modèle des propriétés d'un projet
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




#définit la liste des suffixes possibles pour les lots
LISTE_SUFFIXE=(
		('','Suffixe'),
		('A','A'),
		('B','B'),
		('C','C'),
		('bis','Bis'),
		('ter','Ter'),
	)



#définit la liste des activités possibles des entreprises
LISTE_ACTIVITES =(
		('Façades','Façades'),
		('Electricité','Electricité'),
		('Non renseigné','Non renseigné'),
		('Autre','Autre'),
	)


class DomaineCompetence(models.Model):
	competence=models.CharField(max_length=255,choices=LISTE_ACTIVITES,default="NR")

	def __str__(self):
		return self.competence

	class Meta:
		ordering =['competence']





#définit le modèle des lots
class Lot(models.Model):
	numero=models.IntegerField(verbose_name="Numéro du lot ")
	suffixe=models.CharField(max_length=5,default='',blank=True,choices=LISTE_SUFFIXE,verbose_name="Suffixe")
	description=models.TextField(null=True,blank=True,verbose_name="Description succincte ",help_text="Décrivez de manière succincte les éléments constitutifs du travail à faire")
	short_name=models.CharField(max_length=10,null=True,verbose_name="Nom court pour identifier le lot facilement",help_text="Sera utilisé dans la barre de navigation")
	nom=models.CharField(max_length=255,null=True,verbose_name="Nom du lot ")

	publier=models.BooleanField(default=False)

	projet=models.ForeignKey(Projet,on_delete=models.CASCADE)
	activites=models.ManyToManyField(DomaineCompetence,blank=True)

	class Meta:
		ordering=['numero','suffixe']


	def __str__(self):
		return 'N° ' + str(self.numero) + ' ' + self.suffixe + ' - ' + self.short_name

	def decris_toi(self):
		return ' N°' + str(self.numero) + ' ' + self.suffixe + ' : ' + self.short_name + ' - ' + self.nom



#défini le chemin d'enregistrement des fichiers des lots et créé le chemin si besoin dans le dossier projets
def fichier_lot_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers','projets',str(instance.lot.projet.numero_teamber)+'-'+str(instance.lot.projet.nom),str(instance.lot.nom))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)


#définit la liste des types de fichiers DPGF, CTTP, autres .....
LISTE_CATEGORIE_FICHIER_LOT=(
		('DPGF','DPGF'),
		('CCTP','CCTP'),
		('PLAN','Plan'),
		('DIAG','Diagnostic'),
		('AUTRE','Autre'),
	)

#définit le modèle des documents pour les lots
class DocumentLot(models.Model):
	fichier=models.FileField(upload_to=fichier_lot_path,blank=True,null=True,verbose_name="Document du projet : ",storage=OverwriteStorage())
	categorie=models.CharField(max_length=255,choices=LISTE_CATEGORIE_FICHIER_LOT,default="AUTRE",null=True,blank=True,verbose_name="Catégorie de document")

	lot=models.ForeignKey(Lot,on_delete=models.CASCADE,related_name="documents")

	def nom(self):
		nom=right_path(self.fichier.path,"\\")
		return nom

	def taille(self):
		mem=self.fichier.size/1024
		mem=round(mem)

		return str(mem) + ' Mo'


	def __str__(self):
		return self.fichier.name


def fichier_entreprise_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers','entreprises',str(instance.nom_ent))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)


#définit le modèle de l'entreprise principale
class Entreprise(models.Model):
	nom_ent=models.CharField(max_length=255,blank=True,null=True,verbose_name="Nom de l'entreprise ",unique=True)
	date_inscription_ent=models.DateTimeField(default=datetime.date.today,blank=True,verbose_name="Date d'inscription ")
	date_creation_ent=models.DateTimeField(blank=True,null=True,verbose_name="Date de création de l'entreprise")
	logo_ent=models.ImageField(upload_to=fichier_entreprise_path,blank=True,null=True,verbose_name="Logo de l'entreprise (facultatif) ",storage=OverwriteStorage())
	SIREN_regex=RegexValidator(regex=r'^(?P<siren>\d{9})$',message="Le numéro SIREN doit être composé de 9 chiffres exactement ")
	num_SIREN=models.CharField(validators=[SIREN_regex],max_length=9,null=True,unique=True,verbose_name="N°SIREN (9 premiers chiffres du N°SIRET) ")

	class Meta :
		ordering=['nom_ent']

	def __str__(self):
		return self.nom_ent




LISTE_DEPARTEMENT =(
	('rhone','Rhône'),
	('ain','Ain'),
	('haute savoie','Haute-Savoie'),
	('isere','Isère'),
	('autre','Autre'),
	('NR','Non renseigné'),
	)

LISTE_REGION = (
	('AUV-RN','Auvergne Rhône Alpes'),
	('france','France entière'),
	('autre','Autre'),
	('NR','Non renseigné'),
	)



#définit le/les secteurs geographique d'intervention de l'entreprise
class SecteurGeographique(models.Model):
	departement=models.CharField(max_length=255,choices=LISTE_DEPARTEMENT,default="NR",blank=True)
	region=models.CharField(max_length=255,choices=LISTE_REGION,default="NR",blank=True)

	def __str__(self):
		return 'Secteur geographique ' + self.departement




#défini le chemin d'enregistrement des fichiers des agence et créé le chemin si besoin dans le dossier entreprise
def fichier_agence_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers','entreprises',str(instance.agence.entreprise.nom_ent),str(instance.agence.nom))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)


#défini le chemin d'enregistrement du logo des agence et créé le chemin si besoin dans le dossier entreprise
def image_agence_path(instance,filename):
	path=os.path.join(settings.BASE_DIR,'media','fichiers','entreprises',str(instance.entreprise.nom_ent),str(instance.nom))

	if not os.path.isdir(path):
		print(path,' chemin fichier n\'existe pas')
		os.makedirs(path)

	else :
		print(path, 'chemin fichier existe déjà')

	return os.path.join(path, filename)


#définit la liste des catégories d'agences
LISTE_CAT_AGENCE=(
	('siege','Siege'),
	('antenne','Antenne'),
	)


#définit le modèle de l'agence
class Agence(models.Model):
	nom=models.CharField(max_length=255,verbose_name="Dénomination de l'agence ")
	categorie=models.CharField(max_length=255,choices=LISTE_CAT_AGENCE)
	

	phone_regex=RegexValidator(regex=r'^0(?P<num>\d{9})$',message="Le numéro de téléphone doit contenir exactement 10 chiffres")
	telephone=models.CharField(validators=[phone_regex],max_length=10,blank=True)
	fax=models.CharField(validators=[phone_regex],max_length=10,blank=True)
	mail_contact=models.EmailField(max_length=255)
	logo_agence=models.ImageField(upload_to=image_agence_path,blank=True,null=True,verbose_name="Logo de l'agence si différent (facultatif) ",storage=OverwriteStorage())

	SIRET_regex=RegexValidator(regex=r'^(?P<siret>\d{14})$',message="Le numéro SIRET doit être composé de 14 chiffres")
	num_SIRET=models.CharField(validators=[SIRET_regex],max_length=14,unique=True,null=True,verbose_name="N°SIRET")

	entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE)
	lots=models.ManyToManyField(Lot,related_name="repondants",blank=True)

	competences_agence=models.ManyToManyField(DomaineCompetence,blank=True)
	#secteur_geographique=models

	date_inscription_agence=models.DateTimeField(default=datetime.date.today,verbose_name="Date d'inscription ")
	date_creation_agence=models.DateTimeField(blank=True,null=True,verbose_name="Date de création de l'agence")

	class Meta :
		ordering=['-categorie','nom']

	def __str__(self):
		return 'agence ' + self.nom 








#définit la liste des catégorie de fichier pour les agences d'entreprises
LISTE_CAT_FICHIER_AGENCE=(
		('assurance','Assurance'),
		('RC','Responsabilité civile'),
		('autre','Autre'),
)


#définit le modèle des documents pour les lots
class DocumentAgence(models.Model):
	fichier=models.FileField(upload_to=fichier_agence_path,blank=True,null=True,verbose_name="Document de l'agence : ",storage=OverwriteStorage())
	categorie=models.CharField(max_length=255,choices=LISTE_CAT_FICHIER_AGENCE,default="autre",null=True,blank=True,verbose_name="Catégorie de document")

	agence=models.ForeignKey(Agence,on_delete=models.CASCADE)

	def __str__(self):
		return self.fichier.name


class Personne(models.Model):
	prenom=models.CharField(max_length=255,verbose_name="Prénom ")
	nom=models.CharField(max_length=255,verbose_name="Nom ")
	phone_regex=RegexValidator(regex=r'^0(?P<num>\d{9})$',message="Le numéro de téléphone doit contenir exactement 10 chiffres et commencer par 0")
	portable=models.CharField(validators=[phone_regex],max_length=10,blank=True)
	ligne_directe=models.CharField(validators=[phone_regex],max_length=10,blank=True)
	mail=models.EmailField(max_length=255)
	date_inscription_personne=models.DateTimeField(default=timezone.now(),verbose_name="Date d'inscription ")

	agence=models.ForeignKey(Agence,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return self.nom + ' ' + self.prenom



# définit le modèle Adresse
class Adresse(models.Model):
	adresse1=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Adresse ")
	adresse2=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Complément d'adresse ")
	code_postal=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Code Postal ")
	ville=models.CharField(default="",null=True,blank=True,max_length=255,verbose_name="Ville ")
	pays=models.CharField(default="France",null=True,blank=True,max_length=255,verbose_name="Pays ")

	projet=models.OneToOneField(Projet,on_delete=models.CASCADE,null=True,blank=True)
	agence=models.OneToOneField(Agence,on_delete=models.CASCADE,null=True,blank=True)
	

	def __str__(self):

		if self.projet:
			return 'adresse projet : ' + self.projet.nom
		else:
			if self.agence:
				return 'adresse agence : ' + self.agence.nom
			else:
				return 'adresse non assignée'







class AppelOffre(models.Model):

	projet=models.ForeignKey(Projet,on_delete=models.CASCADE,blank=True)
	lots=models.ManyToManyField(Lot,blank=True)
	numero=models.IntegerField(default=0)

	#createur

	def __str__(self):
		return 'AO par lot du projet ' + self.projet.nom



class AppelOffreLot(models.Model):


	date_lancement=models.DateField(default=datetime.date.today,verbose_name="Date de démarrage de la consultation")
	relance=models.IntegerField(default=0,blank=True,validators=[MaxValueValidator(99)],verbose_name="Intervalle de relance (jours calendaires)")

	AO_agences=models.ManyToManyField(Agence,blank=True)
	AO_personnes=models.ManyToManyField(Personne,blank=True)

	AO=models.ForeignKey(AppelOffre,on_delete=models.CASCADE,blank=True)
	projet=models.ForeignKey(Projet,on_delete=models.CASCADE,blank=True)
	lot=models.ForeignKey(Lot,on_delete=models.CASCADE,blank=True)

	def __str__(self):
		return 'AO' + str(self.projet.numero_teamber) + self.projet.nom + ' _ ' + self.lot.short_name 


class Offre(models.Model):

	AO=models.ForeignKey(AppelOffre,on_delete=models.PROTECT,blank=True)
	agence=models.ForeignKey(Agence,on_delete=models.PROTECT,blank=True)
	personne=models.ForeignKey(Personne,on_delete=models.PROTECT,blank=True)

	def __str__(self):
		return 'Offre de' + personne.nom + ' ' + personne.prenom + 'sur lot ' + AO.lot.numero + ' du projet ' + AO.projet.nom




class AppelOffreGlobal(models.Model):

	projet=models.ForeignKey(Projet,on_delete=models.CASCADE,blank=True)

	def __str__(self):
		return 'AO Global du projet ' + self.projet.nom


class Echeance(models.Model):
	date=models.DateField(verbose_name="Date de fin de la consultation")

	appel=models.OneToOneField(AppelOffre,on_delete=models.CASCADE,null=True)
	appelLot=models.OneToOneField(AppelOffreLot,on_delete=models.CASCADE,null=True)
	projet=models.OneToOneField(Projet,on_delete=models.CASCADE,null=True)
	appelGlobal=models.OneToOneField(AppelOffreGlobal,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return 'date de fin le ' + str(self.date)