from django.db.models import Q
import random
import string



#permet de rechercher un élément d'un groupe à partir de la chaine dans nom ou numero_teamber et ordonne par filtre
def chercherProjet(groupe,filtre,chaine):

	projets=groupe.filter(Q(nom__contains=chaine)|Q(numero_teamber__contains=chaine)).order_by(filtre)
		
	return projets


#permet de vérifier l'existance d'un éléments "chaine" dans une base de données "groupe" de type Domaine Activité censées être unique 
# On retourne vrai ou faux en fonction des cas
def ExistOrNotCompetence(groupe,chaine):

	test=groupe.filter(Q(competence=chaine))

	if test:
		print('objet existe déjà on le retourne')
		return True
	else:
		print('objet n\'existe pas il faut le créer' + str(chaine))
		return False


#Extrait l'extension d'un fichier si char est un .
def right(name,char):
	left,right=name.split(char)
	return right

#extrait la dernière partie d'un path si char est un /
def right_path(name,char):
	elements=name.split(char)

	return elements[len(elements)-1]



#critère de recherche actuel dans les nom sur les agences, personnes et extensions ..
def chercherContact(entreprise,agence,personne,filtre,filtre_type,chaine):

	#initialisation des queryset à vide
	contacts_ent=entreprise.objects.none()
	contacts_agence=agence.objects.none()
	contacts_personne=personne.objects.none()

	#récupération de la liste des objects de contacts sans filtrage
	groupe_ent=entreprise.objects.all()
	groupe_agence=agence.objects.all()
	groupe_personne=personne.objects.all()

	#requete de filtrage par type  de contact
	if filtre_type=='tous':
		q1=Q()
		if filtre == "entreprise":
			#si entreprise alors que entreprise filtré les autres sont nulls
			if groupe_ent:
				contacts_ent=groupe_ent.filter((Q(nom_ent__contains=chaine)|Q(num_SIREN__contains=chaine)))
		elif filtre == "agence":
			if groupe_agence:
				contacts_agence=groupe_agence.filter((Q(nom__contains=chaine)|Q(num_SIRET__contains=chaine)))
		elif filtre == "personne":
			if groupe_personne:
				contacts_personne=groupe_personne.filter((Q(nom__contains=chaine)|Q(prenom__contains=chaine)))
		else:
			#Si tous alors on recherche sur tous
			if groupe_ent:
				contacts_ent=groupe_ent.filter((Q(nom_ent__contains=chaine)|Q(num_SIREN__contains=chaine)))
			if groupe_agence:
				contacts_agence=groupe_agence.filter((Q(nom__contains=chaine)|Q(num_SIRET__contains=chaine)))
			if groupe_personne:
				contacts_personne=groupe_personne.filter((Q(nom__contains=chaine)|Q(prenom__contains=chaine)))

	else:
		qper=Q(agence__entreprise__type_contact__contains=filtre_type)
		qag=Q(entreprise__type_contact__contains=filtre_type)
		qent=Q(type_contact__contains=filtre_type)



		if filtre == "entreprise":
			#si entreprise alors que entreprise filtré les autres sont nulls
			if groupe_ent:
				contacts_ent=groupe_ent.filter((Q(nom_ent__contains=chaine)|Q(num_SIREN__contains=chaine))&qent)
		elif filtre == "agence":
			if groupe_agence:
				contacts_agence=groupe_agence.filter((Q(nom__contains=chaine)|Q(num_SIRET__contains=chaine))&qag)
		elif filtre == "personne":
			if groupe_personne:
				contacts_personne=groupe_personne.filter((Q(nom__contains=chaine)|Q(prenom__contains=chaine))&qper)
		else:
			#Si tous alors on recherche sur tous
			if groupe_ent:
				contacts_ent=groupe_ent.filter((Q(nom_ent__contains=chaine)|Q(num_SIREN__contains=chaine))&qent)
			if groupe_agence:
				contacts_agence=groupe_agence.filter((Q(nom__contains=chaine)|Q(num_SIRET__contains=chaine))&qag)
			if groupe_personne:
				contacts_personne=groupe_personne.filter((Q(nom__contains=chaine)|Q(prenom__contains=chaine))&qper)
		
	return contacts_ent,contacts_agence,contacts_personne



def chercherAgencePourAO(filtre,competences,selected_agences,groupe_agence):
	#création de la condition de filtrage sur les agences
	if len(competences)>0:
		#requete associée au filtrage
		q1=Q()
		for competence in competences:
			q1|=Q(competences_agence__competence__contains=competence)
		q1&=Q(nom__contains=filtre)

		#requete associé à la selection
		q2=Q()
		if len(selected_agences)>0:
			for sel in selected_agences:
				q2|=Q(pk=sel)
		q3=Q(entreprise__type_contact__contains="entreprises")
		agences=groupe_agence.filter((q1|q2)&q3).distinct()
	else:
		if len(selected_agences)>0:
			q=Q()
			for sel in selected_agences:
				q|=Q(pk=sel)
			q|=Q(nom__contains=filtre)
			q1=Q(entreprise__type_contact__contains="entreprises")
			agences=groupe_agence.filter(q&q1)
		else:
			q1=Q(nom__contains=filtre)
			q2=Q(entreprise__type_contact__contains="entreprises")
			agences=groupe_agence.filter(q1&q2)

	return agences



def chercherPersonnePourAO(filtre,competences,selected_personnes,groupe_personne):
	if len(competences)>0:
		#requete de filtrage
		q1=Q(nom__contains=filtre)|Q(prenom__contains=filtre)|Q(agence__nom__contains=filtre)
		q2=Q()
		for competence in competences:
			q2|=Q(agence__competences_agence__competence__contains=competence)
		q3=q1&q2

		#requete de selection
		q4=Q()
		if len(selected_personnes)>0:
			for sel in selected_personnes:
				q4|=Q(pk=sel)
		q5=Q(agence__entreprise__type_contact__contains="entreprises")
		personnes=groupe_personne.filter((q3|q4)&q5).distinct()
	else:
		#requete de filtrage
		q1=Q(nom__contains=filtre)|Q(prenom__contains=filtre)|Q(agence__nom__contains=filtre)

		#requete de selection
		q2=Q()
		if len(selected_personnes)>0:
			for sel in selected_personnes:
				q2|=Q(pk=sel)
		q3=Q(agence__entreprise__type_contact__contains="entreprises")
		personnes=groupe_personne.filter((q1|q2)&q3)

	return personnes



def mdp_gen():
	chaine=''
	N=10
	chaine=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
	
	return chaine