from django.contrib import admin
from .models import Projet,Adresse,Personne,Propriete,Lot,DocumentLot,Entreprise,Agence,DomaineCompetence
from .models import Echeance,AppelOffre,AppelOffreLot,AppelOffreGlobal
# Register your models here.


admin.site.register(Projet)
admin.site.register(Adresse)
admin.site.register(Propriete)
admin.site.register(DocumentLot)
admin.site.register(Lot)
admin.site.register(Entreprise)
admin.site.register(Agence)
admin.site.register(DomaineCompetence)
admin.site.register(Personne)
admin.site.register(Echeance)
admin.site.register(AppelOffre)
admin.site.register(AppelOffreLot)
admin.site.register(AppelOffreGlobal)