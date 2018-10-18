from django.db.models import Q


#permet de rechercher un élément d'un groupe à partir de la chaine dans nom ou numero_teamber et ordonne par filtre
def chercherProjet(self,groupe,filtre,chaine):

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

def right_path(name,char):
	elements=name.split(char)

	return elements[len(elements)-1]
