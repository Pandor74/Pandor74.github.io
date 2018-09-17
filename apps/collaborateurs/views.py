from django.shortcuts import render,redirect
from collaborateurs.forms import ProjetForm,ImageForm
from collaborateurs.models import Projet,Image
from django.core.mail import send_mail
from django.views.generic import ListView


# Create your views here.

def home(request):

	return render(request,'collaborateurs/accueil_col.html')

def deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())


def new_projet(request):
	envoi=False
	

	if request.method=='POST':
		projet=Projet()
		form=ProjetForm(request.POST, request.FILES)
		if form.is_valid():

			envoi=True
			projet=form.save()
			

			return render(request,'collaborateurs/accueil_col.html',locals())

		return render(request,'collaborateurs/nouveau_projet.html',locals())
	else:
		form=ProjetForm()

	return render(request,'collaborateurs/nouveau_projet.html',locals())

def afficher_projets(request):

	projets=Projet.objects.all()
	trie_par_numero=False;

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


class ListeProjets(ListView):
	model=Projet
	context_object_name="projets"
	template_name="collaborateurs/tous_les_projets.html"
	paginate_by=3
	

	def get_context_data(self,**kwargs):
		
		context=super(ListeProjets,self).get_context_data(**kwargs)
		
		context['filtre']=self.kwargs['num']

		return context

	def get_queryset(self,**kwargs):
		if self.kwargs['num']=='1':
			return Projet.objects.order_by('-annee_teamber','-numero_teamber')
		else:
			if self.kwargs['num']=='2':
				 return Projet.objects.order_by('nom')
			else:
				if self.kwargs['num']=='3':
					return Projet.objects.order_by('localisation') #attention ici il faut créer les propriétés nécessaires
				else:
					if self.kwargs['num']=='4':
						return Projet.objects.order_by('date_AO') #attention ici il faut créer les propriétés nécessaires
					else:
						if self.kwargs['num']=='5':
							return Projet.objects.order_by('avancement') #attention ici il faut créer les propriétés nécessaires
		return Projet.objects.order_by('-annee_teamber','-numero_teamber')

		
