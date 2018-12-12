from django.shortcuts import render
from collaborateurs.models import Projet

# Create your views here.

def home(request):
	projets=Projet.objects.all()

	return render(request,'clients/base.html',locals())