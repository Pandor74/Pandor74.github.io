from django.shortcuts import render
from collaborateurs.models import Projet
from django.contrib.auth.decorators import login_required,user_passes_test
from collaborateurs.models import is_col,is_ent,is_client



# Create your views here.

@login_required
@user_passes_test(is_client,login_url='refus',redirect_field_name=None)
def home(request):
	projets=Projet.objects.all()

	return render(request,'clients/base.html',locals())