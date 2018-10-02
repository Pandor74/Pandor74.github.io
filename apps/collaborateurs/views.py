from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.forms import ProjetForm,FiltreForm,AdresseForm,ProprietesForm,LotForm,DocumentForm
from collaborateurs.models import Projet,Adresse,Propriete,Lot,Document
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy,reverse
from collaborateurs.fonction import chercherProjet


# Create your views here.

def home(request):

	return render(request,'collaborateurs/accueil_col.html')

def deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())


def new_projet(request):
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


def modifier_projet(request,pk):
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
	

	
		
def new_lot(request,pk):
	envoi=False
	print(pk)
	print('ok')
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)

	if request.method=='POST':
		lot=Lot()
		formLot=LotForm(request.POST or None,)

		docDPGF=Document()
		docCCTP=Document()
		docAUTRE=Document()
		formDocDPGF=DocumentForm(request.POST,request.FILES)
		formDocCCTP=DocumentForm(request.POST,request.FILES)
		formDocAUTRE=DocumentForm(request.POST,request.FILES)

		if formLot.is_valid():

			envoi=True
			lot=formLot.save(commit=False)
			lot.projet=projet
			lot.save()

			if formDocDPGF.is_valid():
				print('DPGF')
				docDPGF=formDocDPGF.save(commit=False)
				docDPGF.lot=lot
				docDPGF.save()

			if formDocCCTP.is_valid():
				print('CCTP')
				docCCTP=formDocCCTP.save(commit=False)
				docCCTP.lot=lot
				docCCTP.save()

			if formDocAUTRE.is_valid():
				print('AUTRE')
				docAUTRE=formDocAUTRE.save(commit=False)
				docAUTRE.lot=lot
				docAUTRE.save()
			
			

			return redirect('lister_lot',pk=projet.pk)

		return render(request,'collaborateurs/nouveau_lot.html',locals())
	else:
		formLot=LotForm()
		formDocDPGF=DocumentForm(initial={'categorie':'DPGF'})
		formDocCCTP=DocumentForm(initial={'categorie':'CCTP'})
		formDocAUTRE=DocumentForm(initial={'categorie':'AUTRE'})

	return render(request,'collaborateurs/nouveau_lot.html',locals())


def liste_lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)

	lots=Lot.objects.filter(projet=projet)

	return render(request,'collaborateurs/tous_les_lots.html',locals())

	



def Afficher_Lot(request,pk,id):
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	lot=get_object_or_404(Lot,pk=id)

	return render(request,'collaborateurs/lot.html',locals())