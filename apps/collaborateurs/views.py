from django.shortcuts import render,redirect
from collaborateurs.forms import ProjetForm,ImageForm
from collaborateurs.models import Projet,Image


# Create your views here.

def home(request):

	return render(request,'collaborateurs/accueil_col.html')

def deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())


def new_projet(request):
	envoi=False
	projet=Projet()
	form=ProjetForm(request.POST or None, request.FILES,instance=None)

	if form.is_valid():

		envoi=True
		projet=form.save()
		

		return render(request,'collaborateurs/accueil_col.html',locals())

	return render(request,'collaborateurs/nouveau_projet.html',locals())


def afficher_projets(request):

	projets=Projet.objects.all()

	return render(request,'collaborateurs/tous_les_projets.html',locals())


def new_image(request):
	envoi=False
	projet=Image()
	form=ImageForm(request.POST or None, request.FILES)

	if form.is_valid():

		projet=Image()
		projet.nom=form.cleaned_data["nom"]
		projet.fichier=form.cleaned_data["fichier"]
		projet.save()
		envoi=True


	return render(request,'collaborateurs/nouveau_projet.html',locals())