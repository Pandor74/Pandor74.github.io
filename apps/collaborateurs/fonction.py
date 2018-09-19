from django.db.models import Q

def chercherProjet(self,groupe,filtre,chaine):

	projets=groupe.filter(Q(nom__contains=chaine)|Q(numero_teamber__contains=chaine)).order_by(filtre)
		
	return projets
