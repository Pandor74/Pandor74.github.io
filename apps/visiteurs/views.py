from django.shortcuts import render,redirect
from django.urls import re_path

from visiteurs.forms import ConnexionForm

from django.contrib.auth import login,logout,authenticate
from collaborateurs.models import is_col,is_ent,is_client

from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

def home(request):
	return render(request,'visiteurs/base.html')


def Connexion(request):
	error=False
	connexion=False
	if request.user.is_authenticated:
		connexion=True

	if request.method == "POST":

		formConnexion=ConnexionForm(request.POST)
		if formConnexion.is_valid():
			username=formConnexion.cleaned_data["username"]
			password=formConnexion.cleaned_data["password"]
			print('form valid')

			user=authenticate(username=username,password=password)

			if user:
				login(request,user)
				connexion=True
				print(user.get_all_permissions())
				

				if is_col(user):
					return redirect('col_accueil')
				elif is_ent(user):
					return redirect('ent_accueil')
				elif is_client(user):
					return redirect('cli_accueil')
					
			else:
				error=True
				print('pas d"user correspondant')
		else:
			print('form non valide')
	else:
		formConnexion=ConnexionForm()


	
	return render(request,'visiteurs/connexion.html',locals())



def Deconnexion(request):
	print(request.user)
	logout(request)
	deco=True


	return render(request,'visiteurs/base.html',locals())



def Refuser_Acces(request):
	print('accès refusé à : ',request,' pour :',request.user)
	logout(request)
	refus=True


	return render(request,'visiteurs/base.html',locals())