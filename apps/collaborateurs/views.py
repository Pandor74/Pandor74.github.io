from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.forms import ProjetForm,FiltreFormProjet,AdresseForm,ProprietesForm,LotForm,DocumentLotForm,FichiersForm,AgenceForm,EntrepriseForm
from collaborateurs.forms import CompetenceForm,FiltreFormContact,SiretForm,PersonneForm
from collaborateurs.models import Projet,Adresse,Propriete,Lot,DocumentLot,DomaineCompetence,Entreprise,Agence,Personne
from collaborateurs.models import LISTE_ACTIVITES
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin
from django.http import Http404,FileResponse
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy,reverse
from collaborateurs.fonction import chercherProjet,ExistOrNotCompetence,chercherContact

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
			
			

			return redirect('projet/%s' % projet.pk)

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
			


				return render(request,'collaborateurs/projet.html',locals())


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
	lots=Lot.objects.filter(projet=projet)

	return render(request,'collaborateurs/projet.html',locals())
		
def New_Lot(request,pk):



	envoi=False
	print('pk du projet ' + str(pk))
	print('début de création d\'un lot')
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)

	if request.method=='POST':
		lot=Lot()
		formLot=LotForm(request.POST or None,)
		formFichiers=FichiersForm(request.POST or None,)
		formCompetence=CompetenceForm(request.POST or None,)

		docDPGF=DocumentLot()
		docCCTP=DocumentLot()
		docAUTRE=DocumentLot()
		if formCompetence.is_valid():
			print('competence validées')

		if formLot.is_valid() and formCompetence.is_valid():
			print('formulaires validés')
			competences_form=formCompetence.cleaned_data['competences']

			#permet de vérifier l'existance ou non de la compétence et si jamais on l'a créé au besoin
			liste_competences=DomaineCompetence.objects.all()
			for competence in competences_form:
				if ExistOrNotCompetence(liste_competences,competence):
					print('domaine de compétence éxiste déjà on passe')
				else:
					DomaineCompetence.objects.create(competence=competence)
			
					print('création du domaine de compétence inexistant')
			

			


			envoi=True
			lot=formLot.save(commit=False)
			lot.projet=projet
			lot.save()
			
			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for competence in competences_form:
				compvalid=liste_competences.filter(competence=competence).get()
				lot.activites.add(compvalid)


			if formFichiers.is_valid():
				print('fichiers validés')
				print(request.FILES)

				if "fDPGF" in request.FILES:
					print('fichier DPGF associé')
					docDPGF.fichier=request.FILES['fDPGF']
					docDPGF.categorie="DPGF"
					docDPGF.lot=lot
					docDPGF.save()

				if "fCCTP" in request.FILES:
					print('fichier CCTP associé')
					docCCTP.fichier=request.FILES['fCCTP']
					docCCTP.categorie="CCTP"
					docCCTP.lot=lot
					docCCTP.save()

				if "f1" in request.FILES:
					print('fichier annexe 1 associé')
					docCCTP.fichier=request.FILES['f1']
					docCCTP.categorie=formFichiers.cleaned_data['c1']
					docCCTP.lot=lot
					docCCTP.save()

				if "f2" in request.FILES:
					print('fichier annexe 2 associé')
					docCCTP.fichier=request.FILES['f2']
					docCCTP.categorie=formFichiers.cleaned_data['c2']
					docCCTP.lot=lot
					docCCTP.save()

				if "f3" in request.FILES:
					print('fichier annexe 3 associé')
					docCCTP.fichier=request.FILES['f3']
					docCCTP.categorie=formFichiers.cleaned_data['c3']
					docCCTP.lot=lot
					docCCTP.save()

				if "f4" in request.FILES:
					print('fichier annexe 4 associé')
					docCCTP.fichier=request.FILES['f4']
					docCCTP.categorie=formFichiers.cleaned_data['c4']
					docCCTP.lot=lot
					docCCTP.save()

				if "f5" in request.FILES:
					print('fichier annexe 5 associé')
					docCCTP.fichier=request.FILES['f5']
					docCCTP.categorie=formFichiers.cleaned_data['c5']
					docCCTP.lot=lot
					docCCTP.save()

				if "f6" in request.FILES:
					print('fichier annexe 6 associé')
					docCCTP.fichier=request.FILES['f6']
					docCCTP.categorie=formFichiers.cleaned_data['c6']
					docCCTP.lot=lot
					docCCTP.save()

				if "f7" in request.FILES:
					print('fichier annexe 7 associé')
					docCCTP.fichier=request.FILES['f7']
					docCCTP.categorie=formFichiers.cleaned_data['c7']
					docCCTP.lot=lot
					docCCTP.save()

				if "f8" in request.FILES:
					print('fichier annexe 8 associé')
					docCCTP.fichier=request.FILES['f8']
					docCCTP.categorie=formFichiers.cleaned_data['c8']
					docCCTP.lot=lot
					docCCTP.save()

				if "f9" in request.FILES:
					print('fichier annexe 9 associé')
					docCCTP.fichier=request.FILES['f9']
					docCCTP.categorie=formFichiers.cleaned_data['c9']
					docCCTP.lot=lot
					docCCTP.save()

			return redirect('voir_lot',pk=projet.pk,id=lot.pk)

		return render(request,'collaborateurs/nouveau_lot.html',locals())
	else:
		formLot=LotForm()
		formFichiers=FichiersForm()
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/nouveau_lot.html',locals())


def Liste_Lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)

	lots=Lot.objects.filter(projet=projet)

	return render(request,'collaborateurs/tous_les_lots.html',locals())

	



def Afficher_Lot(request,pk,id):
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	lot=get_object_or_404(Lot,pk=id)
	competences=get_list_or_404(DomaineCompetence)

	return render(request,'collaborateurs/lot.html',locals())



#fonction qui permet d'ouvrir un fichier PDF dans le browser... Il faut intégrer le MIMETYPE pour les autres formats de documents qui seront au final téléchargé
def Voir_Fichier_PDF_Lot(request,pk,id,iddoc,nom):

	doc=get_object_or_404(DocumentLot,pk=iddoc)

	try:
		response=FileResponse(open(doc.fichier.path,'rb'),content_type='application/pdf')
		response['Content-Disposition']='inline;filename='+ nom
	except FileNotFoundError:
		raise Http404()
	return response


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