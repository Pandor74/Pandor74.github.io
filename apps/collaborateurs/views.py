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
from collaborateurs.fonction import chercherProjet,ExistOrNotCompetence,chercherContact,chercherAgencePourAO,chercherPersonnePourAO,right
from django.db.models import Q

#copié depuis un site pour l'utilsaition de PyPDF

from PyPDF2 import PdfFileWriter, PdfFileReader

from django.http import HttpResponse



# Create your views here.

def Home(request):
	
	return render(request,'collaborateurs/accueil_col.html')

def Deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())

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
			projet=form.save()
			adresse.projet=projet
			adresse.save()

			propriete=formProp.save()
			propriete.projet=projet
			propriete.save()
			
			

			return redirect('Afficher_Projet',pk=projet.pk)

		return render(request,'collaborateurs/nouveau_projet.html',locals())
	else:
		form=ProjetForm()
		formAdresse=AdresseForm()

	return render(request,'collaborateurs/nouveau_projet.html',locals())

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
			


				return redirect('voir_projet',pk=projet.pk)


		return render(request,'collaborateurs/modifier_projet.html',locals())


	
	formprojet=ProjetForm(instance=projet)
	formproprietes=ProprietesForm(instance=projet.propriete)
	formadresse=AdresseForm(instance=projet.adresse)

	return render(request,'collaborateurs/modifier_projet.html',locals())

#sert a préparer le terrain pour LIsteprojets
class FormListView(ListView,FormMixin):
	def get(self, request, *args, **kwargs):
	    # From ProcessFormMixin
	    form_class = self.get_form_class()
	    self.form = self.get_form(form_class)

	    # From BaseListView
	    self.object_list = self.get_queryset()
	    allow_empty = self.get_allow_empty()
	    if not allow_empty and len(self.object_list) == 0:
	        raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
	                      % {'class_name': self.__class__.__name__})

	    context = self.get_context_data(object_list=self.object_list, form=self.form)
	    return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)

class ListeProjets(FormListView):
	form_class=FiltreFormProjet
	model=Projet
	context_object_name="projets"
	template_name="collaborateurs/tous_les_projets.html"
	paginate_by=10
	

	def post(self,request,*args,**kwargs):
		self.form=FiltreFormProjet(self.request.POST or None,initial={'choice':'nom'},)

		return super(ListeProjets,self).post(request,*args,**kwargs)

	def get_queryset(self,**kwargs):

		form=self.form
		
		if form.is_valid():
			filtre=form.cleaned_data['filtre']
			recherche=form.cleaned_data['search']
			projets=Projet.objects.all()
			projets=chercherProjet(self,projets,filtre,recherche)
		else :
			projets=Projet.objects.all()
		return projets

	def get_context_data(self,**kwargs):
		context=super(ListeProjets,self).get_context_data(**kwargs)
		
		return context

def Afficher_Projet(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	proprietes=projet.propriete
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	return render(request,'collaborateurs/projet.html',locals())
		
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
			
			lot=formLot.save()
			lot.projet=projet
			lot.save()
			
			
			


			return redirect('voir_lot',pk=projet.pk,pklot=lot.pk)

		else:
			return render(request,'collaborateurs/nouveau_lot.html',locals())

	else:
		formLot=LotForm()
	

	return render(request,'collaborateurs/nouveau_lot.html',locals())


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
			

			return redirect('voir_lot',pk=projet.pk,pklot=lot.pk)

		return render(request,'collaborateurs/modifier_parametres_lot.html',locals())
	else:
		formLot=LotForm(instance=lot)
		

	return render(request,'collaborateurs/modifier_parametres_lot.html',locals())



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

		return redirect('voir_lot',pk=projet.pk,pklot=lot.pk)

		return render(request,'collaborateurs/modifier_fichiers_lot.html',locals())
	else:
		formLot=LotForm()
		

		
		nombre=liste_doc_lot.count()

		formFichiers=FichiersForm(liste_doc_lot)




	

	return render(request,'collaborateurs/modifier_fichiers_lot.html',locals())


def Liste_Lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	appels=projet.appeloffre_set.all()

	lots=Lot.objects.filter(projet=projet)

	return render(request,'collaborateurs/tous_les_lots.html',locals())

	



def Afficher_Lot(request,pk,pklot):
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	lot=get_object_or_404(Lot,pk=pklot)
	competences=get_list_or_404(DomaineCompetence)
	appels=projet.appeloffre_set.all()

	appels_lot=AppelOffreLot.objects.filter(lot=lot)

	return render(request,'collaborateurs/lot.html',locals())



#fonction qui permet d'ouvrir un fichier PDF dans le browser... Il faut intégrer le MIMETYPE pour les autres formats de documents qui seront au final téléchargé
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




#permet la création d'une entreprise et de son agence principale sans lier de personne dedans
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

			
			
			
			return redirect('voir_entreprise', pk=entreprise.pk,nom=entreprise.nom_ent)

		return render(request,'collaborateurs/nouvelle_entreprise.html',locals())
	else:
		formAgence=AgenceForm()
		formAdresse=AdresseForm()
		formEntreprise=EntrepriseForm()

	return render(request,'collaborateurs/nouvelle_entreprise.html',locals())


#permet d'afficher une entreprise et ses éléments
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

def Modifier_Entreprise(request,pk,nom):
	entreprise=get_object_or_404(Entreprise,pk=pk)

	

	if request.method == 'POST':
		modif=True
		formEntreprise=EntrepriseForm(request.POST,request.FILES,instance=entreprise)

		if formEntreprise.is_valid():
			
			entreprise=formEntreprise.save()


			return redirect('voir_entreprise',pk=entreprise.pk,nom=entreprise.nom_ent)

		return render(request,'collaborateurs/modifier_entreprise.html',locals())

	formEntreprise=EntrepriseForm(instance=entreprise)


	return render(request,'collaborateurs/modifier_entreprise.html',locals())



#permet de crééer une agence si l'entreprise existe déjà a partir du pk de l'entreprise et de son nom
def Add_Agence(request,pk,nom):

	entreprise=Entreprise.objects.get(pk=pk)


	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		


		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=entreprise.num_SIREN


		formCompetence=CompetenceForm(request.POST or None,)

		if formAgence.is_valid() and formAdresse.is_valid() and formCompetence.is_valid():

			envoi=True


			competences_form=formCompetence.cleaned_data['competences']

			#permet de vérifier l'existance ou non de la compétence et si jamais on l'a créé au besoin
			liste_competences=DomaineCompetence.objects.all()
			for competence in competences_form:
				if ExistOrNotCompetence(liste_competences,competence):
					print('domaine de compétence éxiste déjà on passe')
				else:
					DomaineCompetence.objects.create(competence=competence)
			
					print('création du domaine de compétence inexistant')
			
			adresse=formAdresse.save(commit=False)
			agence=formAgence.save(commit=False)

			agence.entreprise=entreprise
			agence.save()
			adresse.agence=agence
			
			adresse.save()

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for competence in competences_form:
				compvalid=liste_competences.filter(competence=competence).get()
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('voir_agence', pk=agence.pk,nom=agence.nom)

		return render(request,'collaborateurs/nouvelle_agence.html',locals())
	else:
		formAgence=AgenceForm(initial={'num_SIRET':entreprise.num_SIREN})
		formAdresse=AdresseForm()
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/nouvelle_agence.html',locals())


#Permet de créer une personne depuis l'interface entreprise ou agence a partir du pk de l'entreprise ou de l'agence et de son nom
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

				return redirect('voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

			elif entreprise:
				print('création de personne depuis entreprise')
				print(request.POST.get('selectionAgence'))
				agence=entreprise.agence_set.get(pk=request.POST.get('selectionAgence'))
				print(agence)
				contact=formPersonne.save()
				contact.agence=agence
				contact.save()

				return redirect('voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)
				

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


def Afficher_Agence(request,pk,nom):
	agence=get_object_or_404(Agence,nom=nom)
	entreprise=agence.entreprise
	personnes=agence.personne_set.all()
	adresse=agence.adresse
	competences=agence.competences_agence.all()

	return render(request,'collaborateurs/agence.html',locals())


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


			return redirect('voir_agence',pk=agence.pk,nom=agence.nom)

		return render(request,'collaborateurs/modifier_agence.html',locals())

	formAgence=AgenceForm(instance=agence)
	formAdresse=AdresseForm(instance=agence.adresse)



	return render(request,'collaborateurs/modifier_agence.html',locals())


#permet de créér un nouveau et renvoi sur la création d'une agence, d'une entreprise ou les deux en fonction du besoin
def New_Personne(request):

	if request.method=='POST':

		contact=Personne()
		formPersonne=PersonneForm(request.POST or None,)
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
				return redirect('voir_personne',pk=contact.pk,nom=contact.nom,prenom=contact.prenom)
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

					return redirect('associer_nouvelle_agence',siret=siret,pk=contact.pk)

				else:
					print("ni l'agence ni l'entreprise n'existe il faut les créer")
					
					return redirect('associer_nouvelle_entreprise_et_agence',siret=siret,pk=contact.pk)
		else:
			print('test passage')
			return render(request,'collaborateurs/nouvelle_personne.html',locals())
	else:	
		formPersonne=PersonneForm()
		formSiret=SiretForm()

		return render(request,'collaborateurs/nouvelle_personne.html',locals())


def Associer_New_Agence(request,siret,pk):
	envoi=False


	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=siret

		siren=siret[:9]
		
		entreprise=Entreprise.objects.get(num_SIREN=siren)
		

		formCompetence=CompetenceForm(request.POST or None,)

		if formAgence.is_valid() and formAdresse.is_valid() and formCompetence.is_valid():

			envoi=True


			competences_form=formCompetence.cleaned_data['competences']

			#permet de vérifier l'existance ou non de la compétence et si jamais on l'a créé au besoin
			liste_competences=DomaineCompetence.objects.all()
			for competence in competences_form:
				if ExistOrNotCompetence(liste_competences,competence):
					print('domaine de compétence éxiste déjà on passe')
				else:
					DomaineCompetence.objects.create(competence=competence)
			
					print('création du domaine de compétence inexistant')
			
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
			for competence in competences_form:
				compvalid=liste_competences.filter(competence=competence).get()
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('voir_personne', pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

		return render(request,'collaborateurs/associer_nouvelle_agence.html',locals())
	else:
		formAgence=AgenceForm(initial={'num_SIRET':siret})
		formAdresse=AdresseForm()
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/associer_nouvelle_agence.html',locals())



def Associer_New_Entreprise_Et_Agence(request,siret,pk):
	envoi=False
	print('début association nouvelle enrteprise et agence')


	if request.method == 'POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)
		formAgence.num_SIRET=siret

		entreprise=Entreprise()
		formEntreprise=EntrepriseForm(request.POST,request.FILES)


		formCompetence=CompetenceForm(request.POST or None,)

		if formAgence.is_valid() and formAdresse.is_valid() and formEntreprise.is_valid() and formCompetence.is_valid():

			envoi=True


			competences_form=formCompetence.cleaned_data['competences']

			#permet de vérifier l'existance ou non de la compétence et si jamais on l'a créé au besoin
			liste_competences=DomaineCompetence.objects.all()
			for competence in competences_form:
				if ExistOrNotCompetence(liste_competences,competence):
					print('domaine de compétence éxiste déjà on passe')
				else:
					DomaineCompetence.objects.create(competence=competence)
			
					print('création du domaine de compétence inexistant')
			
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

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for competence in competences_form:
				compvalid=liste_competences.filter(competence=competence).get()
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('voir_personne', pk=contact.pk,nom=contact.nom,prenom=contact.prenom)

		return render(request,'collaborateurs/associer_nouvelle_entreprise.html',locals())

	else:
		formAgence=AgenceForm(initial={'num_SIRET':siret})
		formAdresse=AdresseForm()
		formEntreprise=EntrepriseForm(initial={'num_SIREN':siret[:9]})
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/associer_nouvelle_entreprise.html',locals())


def Afficher_Personne(request,pk,nom,prenom):
	personne=get_object_or_404(Personne,pk=pk)
	agence=personne.agence
	entreprise=agence.entreprise
	adresse=agence.adresse
	appels_personne=personne.appeloffrelot_set.all()
	appels_agence=agence.appeloffrelot_set.all()

	
	return render(request,'collaborateurs/personne.html',locals())



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


			return redirect('voir_personne',pk=personne.pk,nom=personne.nom,prenom=personne.prenom)

		return render(request,'collaborateurs/modifier_personne.html',locals())

	formPersonne=PersonneForm(instance=personne)

	#génération des éléments nécessaire pour le select de l'agence
	
	agences=entreprise.agence_set.all()
	liste=[None]*agences.count()
	for i in range(agences.count()):
		liste[i]=(agences[i].pk,agences[i].nom)
		print(liste)


	return render(request,'collaborateurs/modifier_personne.html',locals())


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
		recherche=formFiltre.cleaned_data['search']

		contacts_ent,contacts_agence,contacts_personne=chercherContact(Entreprise,Agence,Personne,filtre,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'collaborateurs/tous_les_contacts.html',locals())


#démarre la création d'un appel d'offres du projet a partir de son pk
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
			AO.projet=projet
			AO.save()

			
			echeance.appel=AO
			echeance.save()
			
			

			#boucle pour ajouter les lots qui ont été séléctionnée dans le formulaire
			for num_lot in liste_lots:
				lotvalid=Lot.objects.get(pk=num_lot)
				AO.lots.add(lotvalid)


			return redirect('voir_ao',pkprojet=projet.pk,pkAO=AO.pk)
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

			#boucle pour ajouter les lots qui ont été séléctionnée dans le formulaire
			for num_lot in liste_lots:
				lotvalid=Lot.objects.get(pk=num_lot)
				AO.lots.add(lotvalid)


			return redirect('voir_ao',pkprojet=projet.pk,pkAO=AO.pk)
		else:

			

			return render(request,'collaborateurs/modifier_ao.html',locals())



	else:
		
		formEcheance=EcheanceForm(instance=AO.echeance)
		formAO=AppelOffreForm(projet,instance=AO)


		return render(request,'collaborateurs/modifier_ao.html',locals())


def Afficher_AO(request,pkprojet,pkAO):
	projet=Projet.objects.get(pk=pkprojet)
	lots=projet.lot_set.all()
	appels=projet.appeloffre_set.all()


	AO=AppelOffre.objects.get(pk=pkAO)
	lots_AO=AO.lots.all()

	return render(request,'collaborateurs/AO.html',locals())


def New_AO_Lot(request,pkprojet,pkAO,pklot):
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
		
		formAOlot=AppelOffreLotForm(request.POST or None, instance=AOlot)
		formEcheance=EcheanceForm(request.POST or None,)


		liste_agences=request.POST.getlist('AO_agences')
		liste_personnes=request.POST.getlist('AO_personnes')

		if formAOlot.is_valid():
			print('AOlot validé')

		if formEcheance.is_valid():
			print('Echeance valide')

		if formAOlot.is_valid() and formEcheance.is_valid():
			print('ok')
			echeance=formEcheance.save()

			AOlot=formAOlot.save(commit=False)
			
			AOlot.save()

			
			echeance.appelLot=AOlot
			echeance.save()
			
			

			#boucle pour ajouter les agences qui ont été séléctionnées dans le formulaire
			for num_agence in liste_agences:
				agencevalid=Agence.objects.get(pk=num_agence)
				AOlot.AO_agences.add(agencevalid)

			#boucle pour ajouter les personnes qui ont été séléctionnées dans le formulaire
			for num_personne in liste_personnes:
				personnevalid=Personne.objects.get(pk=num_personne)
				AOlot.AO_personnes.add(personnevalid)



			return redirect('voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
		else:
			print('non valide')
			

			return render(request,'collaborateurs/nouveau_ao_lot.html',locals())



	else:
		echeance=Echeance()
		formEcheance=EcheanceForm()

		AOlot=AppelOffreLot()
		agences=Agence.objects.none()
		personnes=Personne.objects.none()
		formAOlot=AppelOffreLotForm(agences,personnes)
		

		return render(request,'collaborateurs/nouveau_ao_lot.html',locals())



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
		return redirect('voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
	else:
		return redirect('nouveau_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk)



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


				return redirect('voir_ao_lot',pkprojet=projet.pk,pkAO=AO.pk,pklot=lot.pk,pkAOlot=AOlot.pk)
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
		agences=Agence.objects.all()
		personnes=Personne.objects.all()
		
		formAOlot=AppelOffreLotForm(agences,personnes,instance=AOlot)

		formFiltreAgence=FiltreFormAgenceAO()
		

		return render(request,'collaborateurs/associer_contact_ao_lot.html',locals())




