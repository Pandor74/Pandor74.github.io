from django.contrib import admin
from .models import Projet,Adresse,Propriete,Lot,Document

# Register your models here.


admin.site.register(Projet)
admin.site.register(Adresse)
admin.site.register(Propriete)
admin.site.register(Document)
admin.site.register(Lot)
