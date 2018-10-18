from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.forms import ProjetForm,FiltreForm,AdresseForm,ProprietesForm,LotForm,DocumentLotForm,FichiersForm,AgenceForm,EntrepriseForm
from collaborateurs.forms import CompetenceForm
from collaborateurs.models import Projet,Adresse,Propriete,Lot,DocumentLot,DomaineCompetence,Entreprise,Agence
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin
from django.http import Http404,FileResponse
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy,reverse
from collaborateurs.fonction import chercherProjet,ExistOrNotCompetence

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
	form_class=FiltreForm
	model=Projet
	context_object_name="projets"
	template_name="collaborateurs/tous_les_projets.html"
	paginate_by=10
	

	def post(self,request,*args,**kwargs):
		self.form=FiltreForm(self.request.POST or None,initial={'choice':'nom'},)

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



def New_Entreprise(request):
	envoi=False

	if request.method=='POST':
		adresse=Adresse()
		formAdresse=AdresseForm(request.POST or None,)

		agence=Agence()
		formAgence=AgenceForm(request.POST, request.FILES)

		entreprise=Propriete()
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
			
			adresse.save()

			#boucle pour ajouter les compétences qui ont été séléctionnée dans le formulaire
			for competence in competences_form:
				compvalid=liste_competences.filter(competence=competence).get()
				agence.competences_agence.add(compvalid)

			
			
			
			return redirect('voir_entreprise', nom=entreprise.nom_ent)

		return render(request,'collaborateurs/nouveau_entreprise.html',locals())
	else:
		formAgence=AgenceForm()
		formAdresse=AdresseForm()
		formEntreprise=EntrepriseForm()
		formCompetence=CompetenceForm()

	return render(request,'collaborateurs/nouveau_entreprise.html',locals())



def Afficher_Entreprise(request,nom):
	entreprise=get_object_or_404(Entreprise,nom_ent=nom)

	return render(request,'collaborateurs/entreprise.html',locals())


def Liste_Contact(request):
	entreprises=Entreprise.objects.all()
	agences=Agence.objects.all()


	return render(request,'collaborateurs/tous_les_contacts.html',locals())