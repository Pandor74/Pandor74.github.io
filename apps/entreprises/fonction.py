from django.db.models import Q
import random
import string



def ChercherMesProjets(Projet,personne):

	AO_lots_pers=personne.appeloffrelot_set.all()

	

	q1=Q()
	for AO_lot in AO_lots_pers:
		if AO_lot.statut=="Envoyé":
			q1|=Q(pk=AO_lot.projet.pk)


	liste_projets=Projet.filter(q1)	

	return liste_projets


def ChercherProjetsAgence(Projet,agence):

	AO_lots_agence=agence.appeloffrelot_set.all()

	

	q1=Q()
	for AO_lot in AO_lots_agence:
		if AO_lot.statut=="Envoyé":
			q1|=Q(pk=AO_lot.projet.pk)



	liste_projets=Projet.filter(q1)	

	return liste_projets