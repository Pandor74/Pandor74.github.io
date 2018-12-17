from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.forms import ProjetForm,FiltreFormProjet,AdresseForm,ProprietesForm,LotForm,DocumentLotForm,FichiersForm,AgenceForm,EntrepriseForm
from collaborateurs.forms import CompetenceForm,FiltreFormContact,SiretForm,PersonneForm
from collaborateurs.forms import AppelOffreForm,AppelOffreLotForm,AppelOffreGlobalForm,EcheanceForm
from collaborateurs.forms import FiltreFormAgenceAO,FiltreFormPersonneAO
from collaborateurs.models import Projet,Adresse,Propriete,Lot,DocumentLot,DomaineCompetence,Entreprise,Agence,Personne
from collaborateurs.models import LISTE_ACTIVITES
from collaborateurs.models import AppelOffre,AppelOffreLot,AppelOffreGlobal,Echeance
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin
from django.http import Http404,FileResponse
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy,reverse
from collaborateurs.fonction import mdp_gen,chercherProjet,ExistOrNotCompetence,chercherContact,chercherAgencePourAO,chercherPersonnePourAO,right
from django.db.models import Q
from collaborateurs.models import is_col,is_ent,is_client
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group


#copié depuis un site pour l'utilsaition de PyPDF

from PyPDF2 import PdfFileWriter, PdfFileReader

from django.http import HttpResponse
import random
import string



# Create your views here.
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Home(request):

	return render(request,'collaborateurs/accueil_col.html',locals())





#permet d'initaliser la base de données des competences
def InitDataBase(request):

	for comp in LISTE_ACTIVITES:
		comp_test=DomaineCompetence.objects.filter(competence=comp[0])
		if not comp_test:
			DomaineCompetence.objects.create(competence=comp[0])

	print(DomaineCompetence.objects.all())	

	return redirect('vis_accueil')

#permet de créer la database User de départ avec les 3 comptes
def InitDataBaseUser(request):
	#création collaborateur
	try:
		user_col=User.objects.create_user(username="testeur_col",password="mdptest09")
		personne_col=Personne.objects.create(user=user_col,prenom="prenom col",nom="nom col",mail="col@col.fr")
		try:
			group_col=Group.objects.create(name="collaborateurs")
			group_col.user_set.add(user_col)
		except:
			group_col=Group.objects.get(name="collaborateurs")
			group_col.user_set.add(user_col)
	except:
		user_col=User.objects.get(username="testeur_col")
		group_col=Group.objects.get(name="collaborateurs")
		group_col.user_set.add(user_col)
		print('déjà créé')



	#création client
	try:
		user_cli=User.objects.create_user(username="testeur_cli",password="mdptest09")
		personne_cli=Personne.objects.create(user=user_cli,prenom="prenom cli",nom="nom cli",mail="client@client.fr")
		try:
			group_cli=Group.objects.create(name="clients")
			group_cli.user_set.add(user_cli)
		except:
			group_cli=Group.objects.get(name="clients")
			group_cli.user_set.add(user_cli)
	except:
		user_cli=User.objects.get(username="testeur_cli")
		group_cli=Group.objects.get(name="clients")
		group_cli.user_set.add(user_cli)
		print('déjà créé')

	#création entreprise client
	try:
		ent_cli=Entreprise.objects.create(nom_ent="Entreprise CLIENT",type_contact="clients",num_SIREN="111111111")
	except:
		print('entreprise client existe déjà')

	#création agence client
	try:
		agence_cli=Agence.objects.create(nom="Agence CLIENT",categorie="siege",num_SIRET="11111111111111",mail_contact="client@client.fr",entreprise=ent_cli)
		user_cli.personne.agence=agence_cli
		user_cli.personne.save()
	except:
		print('agence client existe déjà')



	#création entreprise
	try:
		user_ent=User.objects.create_user(username="testeur_ent",password="mdptest09")
		personne_ent=Personne.objects.create(user=user_ent,prenom="prenom ent",nom="nom ent",mail="ent@ent.fr")
		try:
			group_ent=Group.objects.create(name="entreprises")
			group_ent.user_set.add(user_ent)
		except:
			group_ent=Group.objects.get(name="entreprises")
			group_ent.user_set.add(user_ent)
	except:
		user_ent=User.objects.get(username="testeur_ent")
		group_ent=Group.objects.get(name="entreprises")
		group_ent.user_set.add(user_ent)
		print('déjà créé')

	#création entreprise entreprises
	try:
		ent_ent=Entreprise.objects.create(nom_ent="Entreprise ENT",type_contact="entreprises",num_SIREN="222222222")
	except:
		print('entreprise entreprises existe déjà')

	#création agence entreprises
	try:
		agence_ent=Agence.objects.create(nom="Agence ENT",categorie="siege",num_SIRET="22222222222222",mail_contact="ent@ent.fr",entreprise=ent_ent)
		user_ent.personne.agence=agence_ent
		user_ent.personne.save()
	except:
		print('agence entreprises existe déjà')


	print(User.objects.all())

	return redirect('vis_accueil')



#///////////////////////////-------PROJET-------///////////////////////////////////////////////
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_Projet(request):
	envoi=False
	

	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)
		projet=Projet()
		form=ProjetForm(request.POST, request.FILES)
		propriete=Propriete()
		formProp=ProprietesForm(request.POST or None,)
		if form.is_valid() and formAdresse.is_valid() and formProp.is_valid():

			envoi=True
			
			adresse=formAdresse.save()
			projet=form.save(commit=False)
			projet.createur=request.user
			projet.save()
			adresse.projet=projet
			adresse.save()

			propriete=formProp.save()
			propriete.projet=projet
			propriete.save()
			
			

			return redirect('col_voir_projet',pk=projet.pk)

		return render(request,'collaborateurs/nouveau_projet.html',locals())
	else:
		form=ProjetForm()
		formAdresse=AdresseForm()

	return render(request,'collaborateurs/nouveau_projet.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Projet(request,pk):
	modif=False
	oui=False
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()


	if request.method == 'POST':
		modif=True
		formprojet=ProjetForm(request.POST,request.FILES,instance=projet)
		formproprietes=ProprietesForm(request.POST,instance=projet.propriete)
		formadresse=AdresseForm(request.POST,instance=projet.adresse)

		if formproprietes.is_valid() and formadresse.is_valid():
			
			#formprojet.adresse=formadresse.save(commit=False)
			#formprojet.proprietes=formproprietes.save(commit=False)


			print('avant validation projet')
			if formprojet.is_valid():
				print('après validation projet')
				modif=True
				formadresse.save()
				formproprietes.save()
				formprojet.save()
				#projet.photo.save(request.POST.get('photo'),request.FILES['photo'],save=True)
			


				return redirect('col_voir_projet',pk=projet.pk)


		return render(request,'collaborateurs/modifier_projet.html',locals())


	
	formprojet=ProjetForm(instance=projet)
	formproprietes=ProprietesForm(instance=projet.propriete)
	formadresse=AdresseForm(instance=projet.adresse)

	return render(request,'collaborateurs/modifier_projet.html',locals())




@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Liste_Projet(request):

	#on initialise les groupes de contacts qui seront soumis aux filtres
	projets=Projet.objects.all()

	#initilisation du formulaire de filtre des contacts
	formFiltre=FiltreFormProjet(request.POST or None,)

	# Si il y a une requete de filtre alors on appelle la fonction qui filtre les groupes de données
	if formFiltre.is_valid():
		filtre=formFiltre.cleaned_data['filtre']
		recherche=formFiltre.cleaned_data['search']

		projets=chercherProjet(projets,filtre,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'collaborateurs/tous_les_projets.html',locals())




@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Liste_Mes_Projets(request):

	#on initialise les groupes de contacts qui seront soumis aux filtres
	projets=Projet.objects.filter(createur=request.user)

	#initilisation du formulaire de filtre des contacts
	formFiltre=FiltreFormProjet(request.POST or None,)

	# Si il y a une requete de filtre alors on appelle la fonction qui filtre les groupes de données
	if formFiltre.is_valid():
		filtre=formFiltre.cleaned_data['filtre']
		recherche=formFiltre.cleaned_data['search']

		projets=chercherProjet(projets,filtre,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'collaborateurs/tous_les_projets.html',locals())





@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_Projet(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	proprietes=projet.propriete
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	return render(request,'collaborateurs/projet.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_Lot(request,pk):



	envoi=False
	print('pk du projet ' + str(pk))
	print('début de création d\'un lot')
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	if request.method=='POST':
		lot=Lot()
		formLot=LotForm(request.POST or None,)
		


		if formLot.is_valid():
			print('formulaire lot validé')


			envoi=True
			
			lot=formLot.save(commit=False)
			lot.createur=request.user
			lot.projet=projet
			lot.save()
			
			
			


			return redirect('col_voir_lot',pk=projet.pk,pklot=lot.pk)

		else:
			return render(request,'collaborateurs/nouveau_lot.html',locals())

	else:
		formLot=LotForm()
	

	return render(request,'collaborateurs/nouveau_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Lot(request,pk,pklot):



	envoi=False
	print('pk du projet ' + str(pk))
	print('début de modification d\'un lot')
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	lot=get_object_or_404(Lot,pk=pklot)

	if request.method=='POST':

		formLot=LotForm(request.POST or None,instance=lot)
		

		if formLot.is_valid():
			print('formulaires validés')

			envoi=True
			lot=formLot.save()
			

			return redirect('col_voir_lot',pk=projet.pk,pklot=lot.pk)

		return render(request,'collaborateurs/modifier_parametres_lot.html',locals())
	else:
		formLot=LotForm(instance=lot)
		

	return render(request,'collaborateurs/modifier_parametres_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Fichiers_Lot(request,pk,pklot):



	envoi=False
	print('début de modification  des fichiers d\'un lot')
	print('pk du projet ' + str(pk))
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	lot=get_object_or_404(Lot,pk=pklot)
	liste_doc_lot=lot.documents.all()

	if request.method=='POST':
		
		formFichiers=FichiersForm(liste_doc_lot,request.POST or None,)



		if formFichiers.is_valid():
			print('fichiers validés')
			print(request.FILES)
			print(request.POST)

			if "f1" in request.FILES:
				print('fichier annexe 1 associé')
				try:
					docAn1=liste_doc_lot[0]
				except:
					docAn1=DocumentLot()
				docAn1.fichier=request.FILES['f1']
				docAn1.categorie=formFichiers.cleaned_data['c1']
				docAn1.lot=lot
				docAn1.save()
			elif "f1-clear" in request.POST:
				try:
					docAn1=liste_doc_lot[0]
				except:
					docAn1=None
				if docAn1:
					docAn1.delete()

			

			if "f2" in request.FILES:
				print('fichier annexe 2 associé')
				try:
					docAn2=liste_doc_lot[1]
				except:
					docAn2=DocumentLot()
				docAn2.fichier=request.FILES['f2']
				docAn2.categorie=formFichiers.cleaned_data['c2']
				docAn2.lot=lot
				docAn2.save()
			elif "f2-clear" in request.POST:
				try:
					docAn2=liste_doc_lot[1]
				except:
					docAn2=None
				if docAn2:
					docAn2.delete()

			if "f3" in request.FILES:
				print('fichier annexe 3 associé')
				try:
					docAn3=liste_doc_lot[2]
				except:
					docAn3=DocumentLot()
				docAn3.fichier=request.FILES['f3']
				docAn3.categorie=formFichiers.cleaned_data['c3']
				docAn3.lot=lot
				docAn3.save()
			elif "f3-clear" in request.POST:
				try:
					docAn3=liste_doc_lot[2]
				except:
					docAn3=None
				if docAn3:
					docAn3.delete()

			if "f4" in request.FILES:
				print('fichier annexe 4 associé')
				try:
					docAn4=liste_doc_lot[3]
				except:
					docAn4=DocumentLot()
				docAn4.fichier=request.FILES['f4']
				docAn4.categorie=formFichiers.cleaned_data['c4']
				docAn4.lot=lot
				docAn4.save()
			elif "f4-clear" in request.POST:
				try:
					docAn4=liste_doc_lot[3]
				except:
					docAn4=None
				if docAn4:
					docAn4.delete()

			if "f5" in request.FILES:
				print('fichier annexe 5 associé')
				try:
					docAn5=liste_doc_lot[4]
				except:
					docAn5=DocumentLot()
				docAn5.fichier=request.FILES['f5']
				docAn5.categorie=formFichiers.cleaned_data['c5']
				docAn5.lot=lot
				docAn5.save()
			elif "f5-clear" in request.POST:
				try:
					docAn5=liste_doc_lot[4]
				except:
					docAn5=None
				if docAn5:
					docAn5.delete()

			if "f6" in request.FILES:
				print('fichier annexe 6 associé')
				try:
					docAn6=liste_doc_lot[5]
				except:
					docAn6=DocumentLot()
				docAn6.fichier=request.FILES['f6']
				docAn6.categorie=formFichiers.cleaned_data['c6']
				docAn6.lot=lot
				docAn6.save()
			elif "f6-clear" in request.POST:
				try:
					docAn6=liste_doc_lot[5]
				except:
					docAn6=None
				if docAn6:
					docAn6.delete()

			if "f7" in request.FILES:
				print('fichier annexe 7 associé')
				try:
					docAn7=liste_doc_lot[6]
				except:
					docAn7=DocumentLot()
				docAn7.fichier=request.FILES['f7']
				docAn7.categorie=formFichiers.cleaned_data['c7']
				docAn7.lot=lot
				docAn7.save()
			elif "f7-clear" in request.POST:
				try:
					docAn7=liste_doc_lot[6]
				except:
					docAn7=None
				if docAn7:
					docAn7.delete()

			if "f8" in request.FILES:
				print('fichier annexe 8 associé')
				try:
					docAn8=liste_doc_lot[7]
				except:
					docAn8=DocumentLot()
				docAn8.fichier=request.FILES['f8']
				docAn8.categorie=formFichiers.cleaned_data['c8']
				docAn8.lot=lot
				docAn8.save()
			elif "f8-clear" in request.POST:
				try:
					docAn8=liste_doc_lot[7]
				except:
					docAn8=None
				if docAn8:
					docAn8.delete()

			if "f9" in request.FILES:
				print('fichier annexe 9 associé')
				try:
					docAn9=liste_doc_lot[8]
				except:
					docAn9=DocumentLot()
				docAn9.fichier=request.FILES['f9']
				docAn9.categorie=formFichiers.cleaned_data['c9']
				docAn9.lot=lot
				docAn9.save()
			elif "f9-clear" in request.POST:
				try:
					docAn9=liste_doc_lot[8]
				except:
					docAn9=None
				if docAn9:
					docAn9.delete()

		return redirect('col_voir_lot',pk=projet.pk,pklot=lot.pk)

		return render(request,'collaborateurs/modifier_fichiers_lot.html',locals())
	else:
		formLot=LotForm()
		

		
		nombre=liste_doc_lot.count()

		formFichiers=FichiersForm(liste_doc_lot)


	return render(request,'collaborateurs/modifier_fichiers_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Liste_Lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	appels=projet.appeloffre_set.all()

	lots=Lot.objects.filter(projet=projet)

	return render(request,'collaborateurs/tous_les_lots.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_Lot(request,pk,pklot):
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	lot=get_object_or_404(Lot,pk=pklot)
	competences=DomaineCompetence.objects.all()
	appels=projet.appeloffre_set.all()

	appels_lot=AppelOffreLot.objects.filter(lot=lot)
	AOs=AppelOffre.objects.filter(lots=lot)

	return render(request,'collaborateurs/lot.html',locals())


#fonction qui permet d'ouvrir un fichier PDF dans le browser... Il faut intégrer le MIMETYPE pour les autres formats de documents qui seront au final téléchargé
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Voir_Fichier_PDF_Lot(request,pk,pklot,iddoc,nom):

	doc=get_object_or_404(DocumentLot,pk=iddoc)
	extension=doc.get_extension()
	print('extension :',extension)

	if extension =="pdf":
		try:
			response=FileResponse(open(doc.fichier.path,'rb'),content_type='application/pdf')
			response['Content-Disposition']='inline;filename='+ nom
		except FileNotFoundError:
			raise Http404()
		return response
	elif extension == ("jpg" or "jpeg"):
		try:
			response=FileResponse(open(doc.fichier.path,'rb'),content_type='image/jpeg')
			response['Content-Disposition']='inline;filename='+ nom
		except FileNotFoundError:
			raise Http404()
		return response
	elif extension == ("png"):
		try:
			response=FileResponse(open(doc.fichier.path,'rb'),content_type='image/png')
			response['Content-Disposition']='inline;filename='+ nom
		except FileNotFoundError:
			raise Http404()
		return response
	else:
		return Http404()








#///////////////////////////----------CONTACTS--------//////////////////////////////////////////////////









#permet la création d'une entreprise et de son agence principale sans lier de personne dedans
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_Entreprise_Et_Agence(request):
	envoi=False


	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)

		liste=request.POST.getlist('competences_agence')
		print(liste)

		entreprise=Entreprise()
		formEntreprise=EntrepriseForm(request.POST,request.FILES)


		

		if formAgence.is_valid() and formAdresse.is_valid() and formEntreprise.is_valid():

			envoi=True


			adresse=formAdresse.save(commit=False)
			agence=formAgence.save(commit=False)
			entreprise=formEntreprise.save()
			agence.entreprise=entreprise
			agence.save()
			adresse.agence=agence
			
			adresse.save()

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for num_comp in liste:
				compvalid=DomaineCompetence.objects.get(pk=num_comp)
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('col_voir_entreprise', pk=entreprise.pk,nom=entreprise.nom_ent)

		return render(request,'collaborateurs/nouvelle_entreprise.html',locals())
	else:
		formAgence=AgenceForm()
		formAdresse=AdresseForm()
		formEntreprise=EntrepriseForm()

	return render(request,'collaborateurs/nouvelle_entreprise.html',locals())


#permet d'afficher une entreprise et ses éléments
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_Entreprise(request,pk,nom):
	print('afficher entreprise')
	entreprise=get_object_or_404(Entreprise,pk=pk)
	agences=entreprise.agence_set.all()


	#permet de récupérér la liste des personnes inscrites dans les agences de l'entreprise.
	personnes=Personne.objects.none()
	for agence in agences:
		liste_personnes=agence.personne_set.all()
		personnes=personnes.union(liste_personnes)


	return render(request,'collaborateurs/entreprise.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Entreprise(request,pk,nom):
	entreprise=get_object_or_404(Entreprise,pk=pk)

	

	if request.method == 'POST':
		modif=True
		formEntreprise=EntrepriseForm(request.POST,request.FILES,instance=entreprise)

		if formEntreprise.is_valid():
			
			entreprise=formEntreprise.save()


			return redirect('col_voir_entreprise',pk=entreprise.pk,nom=entreprise.nom_ent)

		return render(request,'collaborateurs/modifier_entreprise.html',locals())

	formEntreprise=EntrepriseForm(instance=entreprise)


	return render(request,'collaborateurs/modifier_entreprise.html',locals())


#permet de crééer une agence si l'entreprise existe déjà a partir du pk de l'entreprise et de son nom
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Add_Agence(request,pk,nom):

	entreprise=Entreprise.objects.get(pk=pk)


	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		


		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=entreprise.num_SIREN

		liste=request.POST.getlist('competences_agence')
		print(liste)


		

		if formAgence.is_valid() and formAdresse.is_valid():

			envoi=True

			
			adresse=formAdresse.save(commit=False)
			agence=formAgence.save(commit=False)

			agence.entreprise=entreprise
			agence.save()
			adresse.agence=agence
			
			adresse.save()

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for num_comp in liste:
				compvalid=DomaineCompetence.objects.get(pk=num_comp)
				agence.competences_agence.add(compvalid)

			
			
			return redirect('col_voir_agence', pk=agence.pk,nom=agence.nom)

		return render(request,'collaborateurs/nouvelle_agence.html',locals())
	else:
		formAgence=AgenceForm(initial={'num_SIRET':entreprise.num_SIREN})
		formAdresse=AdresseForm()
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/nouvelle_agence.html',locals())


#Permet de créer une personne depuis l'interface entreprise ou agence a partir du pk de l'entreprise ou de l'agence et de son nom
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Add_Personne(request,pk,nom):

	#on test les deux pour prendre le bon sinon l'autre renvoi None
	try:
		entreprise=Entreprise.objects.get(pk=pk,nom_ent=nom)
	except Entreprise.DoesNotExist:
		entreprise=None

	try:
		agence=Agence.objects.get(pk=pk,nom=nom)
	except Agence.DoesNotExist:
		agence=None



	if request.method=='POST':

		contact=Personne()
		formPersonne=PersonneForm(request.POST or None,)
		formSiret=SiretForm(request.POST or None,)

		if formPersonne.is_valid():
			print('formulaire création de personne validé')
			

			if agence:
				print('création de personne depuis agence')
				contact=formPersonne.save()
				contact.agence=agence
				contact.save()

				#création du compte utilisateur associé
				username=contact.mail
				user=User.objects.create_user(username=username,password="mdptest09",email=contact.mail,first_name=contact.prenom,last_name=contact.nom)
				groupe=Group.objects.get(name=agence.entreprise.type_contact)
				groupe.user_set.add(user)


				return redirect('col_voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

			elif entreprise:
				print('création de personne depuis entreprise')
				print(request.POST.get('selectionAgence'))
				agence=entreprise.agence_set.get(pk=request.POST.get('selectionAgence'))
				print(agence)
				contact=formPersonne.save()
				contact.agence=agence
				contact.save()

				username=contact.mail
				user=User.objects.create_user(username=username,password="mdptest09",email=contact.mail,first_name=contact.prenom,last_name=contact.nom)
				groupe=Group.objects.get(name=entreprise.type_contact)
				groupe.user_set.add(user)

				return redirect('col_voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)
				

		else:
			print('les formulaires ne sont pas valides')
			return render(request,'collaborateurs/ajouter_personne.html',locals())
	else:	
		formPersonne=PersonneForm()

		#génération des éléments nécessaire pour le select de l'agence
		if entreprise:
			agences=entreprise.agence_set.all()
			liste=[None]*agences.count()
			for i in range(agences.count()):
				liste[i]=(agences[i].pk,agences[i].nom)
				print(liste)


			
			

		return render(request,'collaborateurs/ajouter_personne.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_Agence(request,pk,nom):
	agence=get_object_or_404(Agence,nom=nom)
	entreprise=agence.entreprise
	personnes=agence.personne_set.all()
	adresse=agence.adresse
	competences=agence.competences_agence.all()

	return render(request,'collaborateurs/agence.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Agence(request,pk,nom):
	agence=get_object_or_404(Agence,pk=pk,nom=nom)
	ag_competences=agence.competences_agence.all()
	print(ag_competences)
	
	

	if request.method == 'POST':
		modif=True
		formAgence=AgenceForm(request.POST,request.FILES,instance=agence)
		formAdresse=AdresseForm(request.POST,instance=agence.adresse)
		

		liste=request.POST.getlist('competences_agence')
		print(liste)

		if formAgence.is_valid() and formAdresse.is_valid():
			
			envoi=True
			
			adresse=formAdresse.save()
			agence=formAgence.save()

			#boucle pour supprimer les compétences qui ne sont aps dans le formulaire
			for competence in agence.competences_agence.all():
				if competence.pk in liste:
					#rien c'est déjà dedans
					print('nothing')
				else:
					agence.competences_agence.remove(competence)

			#boucle pour ajouter celle qui sont ajoutées
			for num_comp in liste:
				try:
					test=agence.competences_agence.get(pk=num_comp)
				except:
					test=None

				if not test:
					compvalid=DomaineCompetence.objects.get(pk=num_comp)
					agence.competences_agence.add(compvalid)


			return redirect('col_voir_agence',pk=agence.pk,nom=agence.nom)

		return render(request,'collaborateurs/modifier_agence.html',locals())

	formAgence=AgenceForm(instance=agence)
	formAdresse=AdresseForm(instance=agence.adresse)



	return render(request,'collaborateurs/modifier_agence.html',locals())


#permet de créér un nouveau et renvoi sur la création d'une agence, d'une entreprise ou les deux en fonction du besoin
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_Personne(request):

	if request.method=='POST':

		contact=Personne()
		formPersonne=PersonneForm(request.POST or None,)
		formSiret=SiretForm(request.POST or None,)

		if formPersonne.is_valid() and formSiret.is_valid():
			print('formulaire création de personne validé')
			contact=formPersonne.save(commit=False)

			#création du compte utilisateur associé
			username=contact.mail
			user=User.objects.create_user(username=username,password="mdptest09",email=contact.mail,first_name=contact.prenom,last_name=contact.nom)

			contact.user=user
			contact.save()


			siret=formSiret.cleaned_data['num_SIRET']

			try:
				agence=Agence.objects.get(num_SIRET=siret)
				print(agence)
			except:
				print("pas d'agence il faut la créer")
				agence=None

			if agence:
				#l'agence existe on la relie à l'utilisateur
				print("l'agence et l'entreprise existe")
				existance=True
				contact.agence=agence
				groupe=Group.objects.get(name=agence.entreprise.type_contact)
				groupe.user_set.add(user)

				contact.save()
				return redirect('col_voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)
			else:
				siren=siret[:9]
				try:
					entreprise=Entreprise.objects.get(num_SIREN=siren)
					print(entreprise)
				except:
					print("lentreprise n'existe pas il faut la créer")
					entreprise=None

				if entreprise:
					print("l'entreprise existe mais l'agence n'existe pas")
					groupe=Group.objects.get(name=entreprise.type_contact)
					groupe.user_set.add(user)

					return redirect('col_associer_nouvelle_agence',siret=siret,pk=contact.pk)

				else:
					print("ni l'agence ni l'entreprise n'existe il faut les créer")
					
					return redirect('col_associer_nouvelle_entreprise_et_agence',siret=siret,pk=contact.pk)
		else:
			print('test passage')
			return render(request,'collaborateurs/nouvelle_personne.html',locals())
	else:	
		formPersonne=PersonneForm()
		formSiret=SiretForm()

		return render(request,'collaborateurs/nouvelle_personne.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Corriger_Erreur_Personne(request,pk):

	if request.method=='POST':

		contact=get_object_or_404(Personne,pk=pk)
		formPersonne=PersonneForm(request.POST or None,instance=contact)
		formSiret=SiretForm(request.POST or None,)

		if formPersonne.is_valid() and formSiret.is_valid():
			print('formulaire création de personne validé')
			contact=formPersonne.save()

			siret=formSiret.cleaned_data['num_SIRET']

			try:
				agence=Agence.objects.get(num_SIRET=siret)
				print(agence)
			except:
				print("pas d'agence il faut la créer")
				agence=None

			if agence:
				#l'agence existe on la relie à l'utilisateur
				print("l'agence et l'entreprise existe")
				existance=True
				contact.agence=agence
				contact.save()
				return redirect('col_voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)
			else:
				siren=siret[:9]
				try:
					entreprise=Entreprise.objects.get(num_SIREN=siren)
					print(entreprise)
				except:
					print("lentreprise n'existe pas il faut la créer")
					entreprise=None

				if entreprise:
					print("l'entreprise existe mais l'agence n'existe pas")

					return redirect('col_associer_nouvelle_agence',siret=siret,pk=contact.pk)

				else:
					print("ni l'agence ni l'entreprise n'existe il faut les créer")
					
					return redirect('col_associer_nouvelle_entreprise_et_agence',siret=siret,pk=contact.pk)
		else:
			print('test passage')
			return render(request,'collaborateurs/corriger_erreur_personne.html',locals())
	else:
		contact=get_object_or_404(Personne,pk=pk)
		formPersonne=PersonneForm(instance=contact)
		formSiret=SiretForm()

		return render(request,'collaborateurs/corriger_erreur_personne.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Associer_New_Agence(request,siret,pk):
	envoi=False


	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=siret


		liste=request.POST.getlist('competences_agence')
		print(liste)

		siren=siret[:9]
		
		entreprise=Entreprise.objects.get(num_SIREN=siren)
		



		if formAgence.is_valid() and formAdresse.is_valid():

			envoi=True
			
			adresse=formAdresse.save(commit=False)
			agence=formAgence.save(commit=False)
			agence.entreprise=entreprise
			agence.save()
			adresse.agence=agence

			contact=Personne.objects.get(pk=pk)
			print(contact)
			contact.agence=agence
			contact.save()
			
			adresse.save()

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for num_comp in liste:
				compvalid=DomaineCompetence.objects.get(pk=num_comp)
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('col_voir_personne', pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

		return render(request,'collaborateurs/associer_nouvelle_agence.html',locals())
	else:
		formAgence=AgenceForm(initial={'num_SIRET':siret})
		formAdresse=AdresseForm()


	return render(request,'collaborateurs/associer_nouvelle_agence.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Associer_New_Entreprise_Et_Agence(request,siret,pk):
	envoi=False
	print('début association nouvelle enrteprise et agence')


	if request.method == 'POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=siret

		liste=request.POST.getlist('competences_agence')
		print(liste)

		entreprise=Entreprise()
		formEntreprise=EntrepriseForm(request.POST,request.FILES)



		if formAgence.is_valid() and formAdresse.is_valid() and formEntreprise.is_valid():

			envoi=True


			adresse=formAdresse.save(commit=False)
			agence=formAgence.save(commit=False)
			entreprise=formEntreprise.save()
			agence.entreprise=entreprise
			agence.save()
			adresse.agence=agence

			contact=Personne.objects.get(pk=pk)
			print(contact)
			contact.agence=agence
			contact.save()
			
			adresse.save()
			print('début association groupe')
			user=contact.user
			print('user:',user)
			groupe=Group.objects.get(name=entreprise.type_contact)
			print('group:',groupe)
			groupe.user_set.add(user)
			print('group_Qset:',groupe.user_set.all())

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for num_comp in liste:
				compvalid=DomaineCompetence.objects.get(pk=num_comp)
				agence.competences_agence.add(compvalid)


			
			
			
			return redirect('col_voir_personne', pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

		return render(request,'collaborateurs/associer_nouvelle_entreprise.html',locals())

	else:
		formAgence=AgenceForm(initial={'num_SIRET':siret})
		formAdresse=AdresseForm()
		formEntreprise=EntrepriseForm(initial={'num_SIREN':siret[:9]})

	return render(request,'collaborateurs/associer_nouvelle_entreprise.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_Personne(request,pk,nom,prenom):
	personne=get_object_or_404(Personne,pk=pk)
	if personne.agence:
		agence=personne.agence
		entreprise=agence.entreprise
		adresse=agence.adresse
		appels_agence=agence.appeloffrelot_set.all()
	else:
		agence=Agence.objects.none()
		entreprise=Entreprise.objects.none()
		adresse=Adresse.objects.none()
		appels_agence=Agence.objects.none()


	appels_personne=personne.appeloffrelot_set.all()
	

	
	return render(request,'collaborateurs/personne.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_Personne(request,pk,nom,prenom):
	personne=get_object_or_404(Personne,pk=pk)
	agence=personne.agence
	entreprise=agence.entreprise
	

	if request.method == 'POST':
		modif=True
		formPersonne=PersonneForm(request.POST,instance=personne)

		if formPersonne.is_valid():
			
			if request.POST.get('selectionAgence'):
				
				print(agence.pk,'/',request.POST.get('selectionAgence'))
				
				if agence.pk != int(request.POST.get('selectionAgence')):
					nouvelle_agence=Agence.objects.get(pk=request.POST.get('selectionAgence'))
					personne=formPersonne.save()
					personne.agence=nouvelle_agence
					personne.save()
					print("on change d'agence")
				else:
					print("on ne change pas d'agence")
					personne=formPersonne.save()
			else:
				print("il n'y a qu'une agence dans l'entreprise")
				personne=formPersonne.save()


			return redirect('col_voir_personne',pk=personne.pk,nom=personne.nom,prenom=personne.prenom)

		return render(request,'collaborateurs/modifier_personne.html',locals())

	formPersonne=PersonneForm(instance=personne)

	#génération des éléments nécessaire pour le select de l'agence
	
	agences=entreprise.agence_set.all()
	liste=[None]*agences.count()
	for i in range(agences.count()):
		liste[i]=(agences[i].pk,agences[i].nom)
		print(liste)


	return render(request,'collaborateurs/modifier_personne.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Liste_Contact(request):
	#on récupère les valeurs des contacts selon les 3 types définis
	entreprises=Entreprise.objects.all()
	agences=Agence.objects.all()
	personnes=Personne.objects.all()

	#on initialise les groupes de contacts qui seront soumis aux filtres
	contacts_ent=entreprises
	contacts_agence=agences
	contacts_personne=personnes

	#initilisation du formulaire de filtre des contacts
	formFiltre=FiltreFormContact(request.POST or None,)

	# Si il y a une requete de filtre alors on appelle la fonction qui filtre les groupes de données
	if formFiltre.is_valid():
		filtre=formFiltre.cleaned_data['filtre']
		filtre_type=formFiltre.cleaned_data['filtre_type']
		recherche=formFiltre.cleaned_data['search']

		contacts_ent,contacts_agence,contacts_personne=chercherContact(Entreprise,Agence,Personne,filtre,filtre_type,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'collaborateurs/tous_les_contacts.html',locals())
















#///////////////////////////----------APPEL D'OFFRES--------//////////////////////////////////////////////////

#démarre la création d'un appel d'offres du projet a partir de son pk
@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_AO(request,pk):

	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	if request.method=='POST':
		print(request.POST)
		

		AO=AppelOffre(projet=projet)
		formAO=AppelOffreForm(projet,request.POST or None)
		formEcheance=EcheanceForm(request.POST or None,)


		liste_lots=request.POST.getlist('lots')

		if formAO.is_valid():
			print('AO validé')

		if formEcheance.is_valid():
			print('Echeance valide')

		if formAO.is_valid() and formEcheance.is_valid():
			print('ok')
			echeance=formEcheance.save()

			AO=formAO.save(commit=False)
			AO.createur=request.user
			AO.projet=projet
			AO.save()

			
			echeance.appel=AO
			echeance.save()
			
			

			#boucle pour ajouter les lots qui ont été séléctionnée dans le formulaire
			for num_lot in liste_lots:
				lotvalid=Lot.objects.get(pk=num_lot)
				AO.lots.add(lotvalid)

			#pré création des appels d'offres sur les lots sélectionné
			for lot in AO.lots.all():
				if not lot.appeloffrelot_set.filter(AO=AO):
					echeancelot=Echeance.objects.create(date=AO.echeance.date)
					AO_lot=AO.appeloffrelot_set.create(lot=lot,projet=projet,createur=request.user)
					echeancelot.appelLot=AO_lot
					echeancelot.save()



			return redirect('col_voir_ao',pkprojet=projet.pk,pkAO=AO.pk)
		else:
			print('non valide')
			

			return render(request,'collaborateurs/nouveau_ao.html',locals())



	else:
		echeance=Echeance()
		formEcheance=EcheanceForm()

		try:
			der_appel=projet.appeloffre_set.last()
		except:
			der_appel=None

		if der_appel:
			AO=AppelOffre(projet=projet,numero=projet.appeloffre_set.last().numero+1)
		else:
			AO=AppelOffre(projet=projet,numero=1)

		formAO=AppelOffreForm(instance=AO,projet=projet)
		

		return render(request,'collaborateurs/nouveau_ao.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_AO(request,pkprojet,pkAO):
	projet=get_object_or_404(Projet,pk=pkprojet)
	AO=get_object_or_404(AppelOffre,pk=pkAO)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	if request.method=='POST':
		print(request.POST)
		formAO=AppelOffreForm(projet,request.POST or None,instance=AO)
		formEcheance=EcheanceForm(request.POST or None,instance=AO.echeance)


		liste_lots=request.POST.getlist('lots')

		if formAO.is_valid() and formEcheance.is_valid():
			print('ok')
			AO.echeance=formEcheance.save()

			AO=formAO.save()

			

			print(AO.appeloffrelot_set.all())
			print(AO.lots.all())

			#suppression des appels d'offre déselectionné
			for ao_lot in AO.appeloffrelot_set.all():
				if not ao_lot.lot in AO.lots.all():
					ao_lot.delete()
					print('pas dedans') 


			#pré création des appels d'offres sur les lots sélectionné
			for lot in AO.lots.all():
				if not lot.appeloffrelot_set.filter(AO=AO):
					echeancelot=Echeance.objects.create(date=AO.echeance.date)
					AO_lot=AO.appeloffrelot_set.create(lot=lot,projet=projet,createur=request.user)
					echeancelot.appelLot=AO_lot
					echeancelot.save()




			return redirect('col_voir_ao',pkprojet=projet.pk,pkAO=AO.pk)
		else:

			

			return render(request,'collaborateurs/modifier_ao.html',locals())



	else:
		
		formEcheance=EcheanceForm(instance=AO.echeance)
		formAO=AppelOffreForm(projet,instance=AO)


		return render(request,'collaborateurs/modifier_ao.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_AO(request,pkprojet,pkAO):
	projet=Projet.objects.get(pk=pkprojet)
	lots=projet.lot_set.all()
	appels=projet.appeloffre_set.all()


	AO=AppelOffre.objects.get(pk=pkAO)
	AO_lots=AO.appeloffrelot_set.all()

	return render(request,'collaborateurs/AO.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Lister_AO(request,pkprojet):
	projet=get_object_or_404(Projet,pk=pkprojet)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	liste_AO=projet.appeloffre_set.all()


	return render(request,'collaborateurs/lister_AO.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def New_AO_Lot(request,pkprojet,pkAO,pklot):
	#requetes pour navigation
	projet=get_object_or_404(Projet,pk=pkprojet)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	AO=get_object_or_404(AppelOffre,pk=pkAO)
	lot=get_object_or_404(Lot,pk=pklot)

	if request.method=='POST':
		print(request.POST)
		
		AOlot=AppelOffreLot()
		AOlot.lot=lot
		AOlot.AO=AO
		AOlot.projet=projet
		agences=Agence.objects.none()
		personnes=Personne.objects.none()
		
		formAOlot=AppelOffreLotForm(agences,personnes,request.POST or None, instance=AOlot)
		formEcheance=EcheanceForm(request.POST or None,)


		if formAOlot.is_valid():
			print('AOlot validé')

		if formEcheance.is_valid():
			print('Echeance valide')

		if formAOlot.is_valid() and formEcheance.is_valid():
			print('ok')
			echeance=formEcheance.save()

			AOlot=formAOlot.save(commit=False)
			AOlot.createur=request.user
			
			AOlot.save()

			
			echeance.appelLot=AOlot
			echeance.save()

			return redirect('col_voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
		else:
			print('non valide')
			

			return render(request,'collaborateurs/nouveau_ao_lot.html',locals())



	else:
		echeance=Echeance()
		formEcheance=EcheanceForm(instance=AO.echeance)

		AOlot=AppelOffreLot()
		agences=Agence.objects.none()
		personnes=Personne.objects.none()
		formAOlot=AppelOffreLotForm(agences,personnes)
		

		return render(request,'collaborateurs/nouveau_ao_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Afficher_AO_Lot(request,pkprojet,pkAO,pklot,pkAOlot):
	projet=Projet.objects.get(pk=pkprojet)
	lots=projet.lot_set.all()
	appels=projet.appeloffre_set.all()

	lot=Lot.objects.get(pk=pklot)


	AO=AppelOffre.objects.get(pk=pkAO)
	AOlot=AppelOffreLot.objects.get(pk=pkAOlot)

	agences=AOlot.AO_agences.all()
	personnes=AOlot.AO_personnes.all()

	return render(request,'collaborateurs/AO_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Modifier_AO_Lot(request,pkprojet,pkAO,pklot,pkAOlot):
	projet=get_object_or_404(Projet,pk=pkprojet)
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	AO=get_object_or_404(AppelOffre,pk=pkAO)
	lot=get_object_or_404(Lot,pk=pklot)
	AOlot=get_object_or_404(AppelOffreLot,pk=pkAOlot)
	echeance=AOlot.echeance

	if request.method=='POST':
		print(request.POST)
		

		agences=Agence.objects.none()
		personnes=Personne.objects.none()
		
		formAOlot=AppelOffreLotForm(agences,personnes,request.POST or None, instance=AOlot)
		formEcheance=EcheanceForm(request.POST or None,instance=echeance)


		if formAOlot.is_valid():
			print('AOlot validé')

		if formEcheance.is_valid():
			print('Echeance valide')

		if formAOlot.is_valid() and formEcheance.is_valid():
			print('ok')
			formEcheance.save()

			formAOlot.save(commit=False)


			return redirect('col_voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
		else:
			print('non valide')
			

			return render(request,'collaborateurs/modifier_ao_lot.html',locals())



	else:

		formEcheance=EcheanceForm(instance=echeance)


		agences=Agence.objects.none()
		personnes=Personne.objects.none()
		formAOlot=AppelOffreLotForm(agences,personnes,instance=AOlot)
		

		return render(request,'collaborateurs/modifier_ao_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Gerer_AO_Lot(request,pkprojet,pkAO,pklot):
	projet=Projet.objects.get(pk=pkprojet)
	lots=projet.lot_set.all()
	appels=projet.appeloffre_set.all()

	lot=Lot.objects.get(pk=pklot)


	AO=AppelOffre.objects.get(pk=pkAO)
	lots_AO=AO.lots.all()

	try:
		AOlot=AppelOffreLot.objects.get(AO=AO,lot=lot)
	except:
		AOlot=None

	if AOlot:
		return redirect('col_voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
	else:
		return redirect('col_nouveau_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk)


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Selectionner_Contact_AO_Lot(request,pkprojet,pkAO,pklot,pkAOlot):

	projet=get_object_or_404(Projet,pk=pkprojet)
	
	#requetes pour la navigation a gauche
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()


	AO=get_object_or_404(AppelOffre,pk=pkAO)
	lot=get_object_or_404(Lot,pk=pklot)
	AOlot=get_object_or_404(AppelOffreLot,pk=pkAOlot)

	if request.method=='POST':

		#on vérifie si la personne a appuyé sur le bouton filtrer
		try:
			filtrage=request.POST.get('Bfiltrer')
		except:
			filtrage=None

		#On vérifie si la personne a appuyé sur le bouton selectionner
		try:
			selection=request.POST.get('Bselect')
		except:
			selection=None

		#si il n'y a pas filtrage mais selection alors on enregistre le tout
		if not filtrage and selection:
			print('données de post')
			print(request.POST)


			#gestion du fitrage

			formFiltreAgence=FiltreFormAgenceAO(request.POST or None,)
			
			filtre=request.POST.get('search')
			competences=request.POST.getlist('competences')
			selected_agences=request.POST.getlist('AO_agences')
			selected_personnes=request.POST.getlist('AO_personnes')
			print('filtre :',filtre)
			print('competences :',competences)
			print('selected agences :',selected_agences)
			print('selected personnes :',selected_agences)
			print('POST :',request.POST)
			
			#création de la condition de filtrage sur les agences
			
			agences=chercherAgencePourAO(filtre,competences,selected_agences,Agence.objects.all())
			
			print(agences)
			#création de la condition de filtrage sur les personnes
			personnes=chercherPersonnePourAO(filtre,competences,selected_personnes,Personne.objects.all())
			
			
			formAOlot=AppelOffreLotForm(agences,personnes,request.POST or None, instance=AOlot)
			

			liste_agences=request.POST.getlist('AO_agences')
			liste_personnes=request.POST.getlist('AO_personnes')
			

			if formAOlot.is_valid():
				print('AOlot validé')

				AOlot=formAOlot.save()

				#boucle pour ajouter les agences qui ont été séléctionnées dans le formulaire
				for num_agence in liste_agences:
					agencevalid=Agence.objects.get(pk=num_agence)
					AOlot.AO_agences.add(agencevalid)

				#récupère la liste des personnes déjà enregistrées
				personnes=AOlot.AO_personnes.all()


				#boucle pour ajouter les personnes qui ont été séléctionnées dans le formulaire
				for num_personne in liste_personnes:
					personnevalid=Personne.objects.get(pk=num_personne)
					AOlot.AO_personnes.add(personnevalid)


				return redirect('col_voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
			else:
				print('non valide')
				

				return render(request,'collaborateurs/associer_contact_ao_lot.html',locals())

		else:
			#On a appuyé sur le bouton de filtrage et pas sur le bouton selection
			
			

			formFiltreAgence=FiltreFormAgenceAO(request.POST or None,)

			if formFiltreAgence.is_valid():

				#gestion du fitrage
				filtre=request.POST.get('search')
				competences=request.POST.getlist('competences')
				selected_agences=request.POST.getlist('AO_agences')
				selected_personnes=request.POST.getlist('AO_personnes')
				print('filtre :',filtre)
				print('competences :',competences)
				print('selected agences :',selected_agences)
				print('selected personnes :',selected_agences)
				print('POST :',request.POST)
				
				#création de la condition de filtrage sur les agences
				agences=chercherAgencePourAO(filtre,competences,selected_agences,Agence.objects.all())

				print(agences)
					
				#création de la condition de filtrage sur les personnes
				personnes=chercherPersonnePourAO(filtre,competences,selected_personnes,Personne.objects.all())
				

				
				formAOlot=AppelOffreLotForm(agences,personnes,request.POST or None, instance=AOlot)
				
				return render(request,'collaborateurs/associer_contact_ao_lot.html',locals())
			
			else:
				agences=Agence.objects.all()
				personnes=Personne.objects.all()
		
				formAOlot=AppelOffreLotForm(agences,personnes,instance=AOlot)
				formFiltreAgence=FiltreFormAgenceAO()

				return render(request,'collaborateurs/associer_contact_ao_lot.html',locals())
	else:
		#à filtrer en fonction du type client/entreprise
		filtre=''
		competences=DomaineCompetence.objects.filter(lot=lot)
		print(competences)
		selected_agences=Agence.objects.none()
		selected_personnes=Personne.objects.none()

		agences=chercherAgencePourAO(filtre,competences,selected_agences,Agence.objects.all())
		personnes=chercherPersonnePourAO(filtre,competences,selected_personnes,Personne.objects.all())
		
		formAOlot=AppelOffreLotForm(agences,personnes,instance=AOlot)

		list_comp=['']*competences.count()
		i=0
		for comp in competences:
			list_comp[i]=comp.competence
			i+=1

		formFiltreAgence=FiltreFormAgenceAO(initial={'competences':list_comp})

		

		

		return render(request,'collaborateurs/associer_contact_ao_lot.html',locals())


@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Valider_AO_Lot(request,pkprojet,pkAO,pklot,pkAOlot):
	projet=get_object_or_404(Projet,pk=pkprojet)
	
	#requetes pour la navigation a gauche
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()


	lot=Lot.objects.get(pk=pklot)


	AO=AppelOffre.objects.get(pk=pkAO)
	AOlot=get_object_or_404(AppelOffreLot,pk=pkAOlot)

	agences=AOlot.AO_agences.all()
	personnes=AOlot.AO_personnes.all()


	
	AOlot.statut='Validé'
	AOlot.save()
	validation_lot=True

	return render(request,'collaborateurs/AO_lot.html',locals())



@login_required
@user_passes_test(is_col,login_url='refus',redirect_field_name=None)
def Publier_AO(request,pkprojet,pkAO):
	projet=get_object_or_404(Projet,pk=pkprojet)
	
	#requetes pour la navigation a gauche
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	AO=get_object_or_404(AppelOffre,pk=pkAO)
	AO_lots=AO.appeloffrelot_set.all()

	AO_non_valide=False

	for AO_lot in AO_lots:
		if AO_lot.statut =='En création':
			AO_non_valide=True

	if not AO_non_valide:
		#tous les AO sont validé ou déjà envoyé
		deja_envoye=False
		for AO_lot in AO_lots:
			if AO_lot.statut=='Validé':
				#call function envoyer mail a toutes les agences et personnes

				AO_lot.statut='Envoyé'
				AO_lot.save()
				
			else:
				#cet ao est déjà envoyé ne rien faire
				deja_envoye=True

		
		return render(request,'collaborateurs/publication_AO.html',locals())


	else:
		#un AO n'est pas validé message erreur le signifiant en rouge dans la liste des AO_lot

		return render(request,'collaborateurs/AO.html',locals())