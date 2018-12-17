
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from collaborateurs.models import Projet,Lot,AppelOffre,AppelOffreLot,DomaineCompetence,DocumentLot

from collaborateurs.forms import ProjetForm,FiltreFormProjet,AdresseForm,ProprietesForm,LotForm,DocumentLotForm,FichiersForm,AgenceForm,EntrepriseForm
from collaborateurs.forms import CompetenceForm,FiltreFormContact,SiretForm,PersonneForm
from collaborateurs.forms import AppelOffreForm,AppelOffreLotForm,AppelOffreGlobalForm,EcheanceForm
from collaborateurs.forms import FiltreFormAgenceAO,FiltreFormPersonneAO


from entreprises.models import Offre
from entreprises.fonction import ChercherMesProjets,ChercherProjetsAgence

from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin

from django.http import Http404,FileResponse,HttpResponse
from collaborateurs.models import is_col,is_ent,is_client
from django.contrib.auth.decorators import login_required,user_passes_test


import os
import zipfile
import io


# Create your views here. ENTREPRISE
@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def home(request):
	projets=Projet.objects.all()
	return render(request,'entreprises/base.html',locals())





@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
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
	return render(request,'entreprises/tous_les_projets.html',locals())


@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def Liste_Mes_Projets(request):

	#on initialise les groupes de contacts qui seront soumis aux filtres
	user=request.user
	personne=user.personne
	

	AO_lots=AppelOffreLot.objects.all()
	tous_projets=Projet.objects.all()

	projets=ChercherMesProjets(tous_projets,personne)

	#initilisation du formulaire de filtre des contacts
	formFiltre=FiltreFormProjet(request.POST or None,)

	# Si il y a une requete de filtre alors on appelle la fonction qui filtre les groupes de données
	if formFiltre.is_valid():
		filtre=formFiltre.cleaned_data['filtre']
		recherche=formFiltre.cleaned_data['search']

		projets=chercherProjet(projets,filtre,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'entreprises/tous_les_projets.html',locals())



@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def Liste_Projets_Mon_Agence(request):

	#on initialise les groupes de contacts qui seront soumis aux filtres
	user=request.user
	personne=user.personne
	

	AO_lots=AppelOffreLot.objects.all()
	tous_projets=Projet.objects.all()

	projets=ChercherProjetsAgence(tous_projets,personne)

	#initilisation du formulaire de filtre des contacts
	formFiltre=FiltreFormProjet(request.POST or None,)

	# Si il y a une requete de filtre alors on appelle la fonction qui filtre les groupes de données
	if formFiltre.is_valid():
		filtre=formFiltre.cleaned_data['filtre']
		recherche=formFiltre.cleaned_data['search']

		projets=chercherProjet(projets,filtre,recherche)


	#si il n'y a pas de requete de filtrage alors on affiche tout
	return render(request,'entreprises/tous_les_projets.html',locals())


@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def Afficher_Projet(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	proprietes=projet.propriete
	lots=Lot.objects.filter(projet=projet)
	appels=projet.appeloffre_set.all()

	return render(request,'entreprises/projet.html',locals())

@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def Liste_Lot(request,pk):
	projet=get_object_or_404(Projet,pk=pk)
	appels=projet.appeloffre_set.all()

	lots=Lot.objects.filter(projet=projet)

	return render(request,'entreprises/tous_les_lots.html',locals())

@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
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
@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
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

@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
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



@login_required
@user_passes_test(is_ent,login_url='refus',redirect_field_name=None)
def Deposer_Fichiers_Offre(request,pkprojet,pklot,pkAO,pkAOlot):


	return render(request,'entreprises/modifier_fichiers_offre.html',locals())


