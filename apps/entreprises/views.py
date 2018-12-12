
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.models import Projet,Lot,AppelOffre,AppelOffreLot,DomaineCompetence,DocumentLot

from collaborateurs.forms import ProjetForm,FiltreFormProjet,AdresseForm,ProprietesForm,LotForm,DocumentLotForm,FichiersForm,AgenceForm,EntrepriseForm
from collaborateurs.forms import CompetenceForm,FiltreFormContact,SiretForm,PersonneForm
from collaborateurs.forms import AppelOffreForm,AppelOffreLotForm,AppelOffreGlobalForm,EcheanceForm
from collaborateurs.forms import FiltreFormAgenceAO,FiltreFormPersonneAO


from entreprises.models import Offre

from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin

from django.http import Http404,FileResponse,HttpResponse

import os
import zipfile
import io


# Create your views here. ENTREPRISE

def home(request):
	projets=Projet.objects.all()
	return render(request,'entreprises/base.html',locals())


def Deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())


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
	template_name="entreprises/tous_les_projets.html"
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

	return render(request,'entreprises/projet.html',locals())


def Liste_Lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	appels=projet.appeloffre_set.all()

	lots=Lot.objects.filter(projet=projet)

	return render(request,'entreprises/tous_les_lots.html',locals())


def Afficher_Lot(request,pk,pklot):
	projet=get_object_or_404(Projet,pk=pk)
	lots=Lot.objects.filter(projet=projet)
	lot=get_object_or_404(Lot,pk=pklot)
	competences=get_list_or_404(DomaineCompetence)
	appels=projet.appeloffre_set.all()

	appels_lot=lot.appeloffrelot_set.all()
	current_user=request.user


	#attention il va falloir modifier lors de l'intégration des utilisateurs
	nombre_appel=appels_lot.count()

	offres=[None]*nombre_appel
	i=0

	for appel_lot in appels_lot:
		offres[i]=Offre()
		offres[i].lot=lot
		offres[i].appel_lot=appel_lot
		offres[i].save()
		i+=1
	

	appels_lot=AppelOffreLot.objects.filter(lot=lot)

	return render(request,'entreprises/lot.html',locals())


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


def Get_Zipped_Files(request,pkprojet,pklot):
	lot=get_object_or_404(Lot,pk=pklot)
	documents=lot.documents.all()
	nombre=documents.count()
	liste_doc=['']*nombre
	i=0
	for doc in documents:
		liste_doc[i]=doc.fichier.path
		i+=1

	zip_subdir=lot.nom
	zip_filename="%s.zip" % zip_subdir

	s=io.BytesIO()

	print(s)
	zf=zipfile.ZipFile(s,"w")

	for path in liste_doc:
		fdir, fname=os.path.split(path)
		zip_path = os.path.join(zip_subdir,fname)

		zf.write(path,zip_path)

	zf.close()

	resp=HttpResponse(s.getvalue(),content_type="application/x-zip-compressed")
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	print(liste_doc)

	return resp




def Deposer_Fichiers_Offre(request,pkprojet,pklot,pkAO,pkAOlot):


	return render(request,'entreprises/modifier_fichiers_offre.html',locals())