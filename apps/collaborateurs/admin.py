from django.contrib import admin
from .models import Projet,Adresse,Propriete,Lot,DocumentLot,Entreprise,Agence,DomaineCompetence

# Register your models here.


admin.site.register(Projet)
admin.site.register(Adresse)
admin.site.register(Propriete)
admin.site.register(DocumentLot)
admin.site.register(Lot)
admin.site.register(Entreprise)
admin.site.register(Agence)
admin.site.register(DomaineCompetence)