from django.shortcuts import render,redirect


# Create your views here.

def home(request):

	return render(request,'collaborateurs/accueil_col.html')

def deconnexion(request):
	deco=True

	return render(request,'visiteurs/base.html',locals())