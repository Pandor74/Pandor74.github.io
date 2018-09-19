"""plateforme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from collaborateurs import views
from django.views.generic import ListView
from .models import Projet
from django.conf.urls import url

urlpatterns = [
	path('',views.home,name='accueil_col'),
	path('deconnexion',views.deconnexion,name='deconnexion'),
	path('nouveau_projet',views.new_projet,name="nouveau_projet"),
    re_path('projets/',views.ListeProjets.as_view(),name="projets_liste"),
    url(r'^projet/(?P<pk>\d+)$',views.VoirProjet.as_view(),name="voir_projet"),
]