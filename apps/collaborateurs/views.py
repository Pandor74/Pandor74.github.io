from django.shortcuts import render,redirect
from collaborateurs.forms import ProjetForm,ImageForm,FiltreForm
from collaborateurs.models import Projet,Image
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy,reverse


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
	paginate_by=3
	

	def post(self,request,*args,**kwargs):
		self.form=FiltreForm(self.request.POST or None,)
		#if self.form.is_valid():
			#projets=Projet.objects.all()
			#return super(ListeProjets,self).post(request,*args,**kwargs)
		#else:
		return super(ListeProjets,self).post(request,*args,**kwargs)

	def get_queryset(self,**kwargs):

		form=self.form

		if form.is_valid():
			if form.cleaned_data['filtre']=='numero':
				projets = Projet.objects.filter().order_by('-annee_teamber','-numero_teamber')
			else:
				projets = Projet.objects.filter().order_by(form.cleaned_data['filtre'])
		else :
			projets=Projet.objects.all()
		return projets

	def get_context_data(self,**kwargs):
		context=super(ListeProjets,self).get_context_data(**kwargs)
		form=context['form']
		context['form']=form




		return context



	

	


	
	

	

		
