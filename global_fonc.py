### par Grégory SCHAAF ###

from dnb import *
import random
import linecache
import sys
import time
import os

try:

	def verifier_permission():
		try:
			w = open("permission.test", "w")
			w.write("")
			w.close()
			os.system("rm permission.test")
		except PermissionError:
			commande_erreur("SUDO", 0, 4)


	def commande_erreur(texte, intervalle_debut, intervalle_fin):
		nb_car = len(texte)
		print("\033[0m" + (" " * centrer(nb_car, None)[0]) + "[" + texte[:intervalle_debut] + "\033[45m" + texte[intervalle_debut:intervalle_fin] + "\033[0m" + texte[intervalle_fin:] + "]\n")
		sys.exit()


	def supprimer_retour_ligne(liste):
		for i in range(len(liste)):
			if liste[i][-1] == "\n":
				liste[i] = liste[i][:-1]

		return liste


	def centrer(taille_element, largeur):
		if largeur == None:
			largeur = os.get_terminal_size()[0]

		cote = (largeur - taille_element) / 2

		if str(cote)[-1] == "5":
			return [int(cote), int(cote) + 1]
		else:
			return [int(cote), int(cote)]


	def legal(programme):
		if programme == "ignis" or programme == "promethei":
			a = open("legal_" + programme + ".log", "a")
			a.write("")
			a.close()
			log = open("legal_" + programme + ".log", "r")
			log = log.read()

			if log != "1" and log != "1\n":
				largeur = centrer(37, None)
				print("\nCe programme a été créé dans un but d'éducation. En acceptant vous conscentez \
à être la seule personne responsable de toute action causée par la copie de ce programme. Avant \
toute utilisation Vous êtes invité à vous renseigner sur les lois de votre pays de résidence et à \
les respecter scrupuleusement.")
				print("\nThis program was created for educational purposes. By accepting, you consent \
to being the sole person responsible for any actions caused by copying this program. \
Before any use, you are invited to familiarize yourself with the laws of your \
country of residence and to scrupulously respect them.")
				print("\nAcceptez-vous les conditions ci-dessus ?")
				print("Do you accept the above conditions?")
				print("1 pour oui (1 for yes) | autre touche pour non (other for no) : ")
				choix = str(input(""))

				if choix.lower() == "1":
					w = open("legal_" + programme + ".log", "w")
					w.write("1")
					w.close()
				else:
					exit()
		else:
			exit()


	def verifier_existence_fichier(chemin_fichier, retour):
		try:
			r = open(chemin_fichier, "r")
			contenu = r.readlines()

			if retour == True:
				return contenu
		except FileNotFoundError:
			commande_erreur(chemin_fichier, 0, len(chemin_fichier))


	def configurer_generation(tuple_verif, option, nom_option):
		liste_type = []
		liste_mot = []
		liste_taille = []
		liste_generation = analyser_separation(nom_option, 0, option, "+", 0)
		liste_nb_mot = [0] * len(liste_generation)
		intervalle_debut = 0
		liste_decoupe_mot = []

		for i in range(len(liste_generation)):
			nom_option_precision = nom_option + "/" + str(i + 1) + ".g ->"
			id_mot = 0
			liste_mot.append(analyser_separation(nom_option_precision, 0, liste_generation[i], ",", 0))

			if liste_mot[i][-1][0] == "/":
				liste_taille.append(liste_mot[i][-2])
				liste_decoupe_mot.append(liste_mot[i][-1])
				liste_mot[i] = liste_mot[i][:-2]
			else:
				liste_taille.append(liste_mot[i][-1])
				liste_decoupe_mot.append(None)
				liste_mot[i] = liste_mot[i][:-1] if len(liste_mot[i]) > 1 else liste_mot[i]

			if liste_mot[i][0][:2] in ('a=', 'p=', 'c=', 'C=', 'f='):
				liste_type.append(liste_mot[i][0][:1])
				liste_mot[i][0] = liste_mot[i][0][2:]
			elif liste_mot[i][0][:2] not in ('a=', 'p=', 'c=', 'C=', 'f=') and "=" in liste_mot[i][0]:
				commande_erreur(nom_option + " " + option, len(nom_option) + 1 + intervalle_debut, len(nom_option) + 1 + intervalle_debut + liste_generation[i].index("=") + 1)
			elif liste_mot[i][0][:2] not in ('a=', 'p=', 'c=', 'C=', 'f=') and "=" not in liste_mot[i][0]:
				commande_erreur(nom_option + " " + option, len(nom_option) + 1 + intervalle_debut, len(nom_option) + 1 + intervalle_debut + len(liste_generation[i]))

			for taille in liste_taille[i]:
				commande_erreur(nom_option + " " + liste_generation[i], len(nom_option) + 1 + (liste_generation[i]).index("," + str(liste_taille[i])) + 1, len(nom_option) + 1 + len(liste_generation[i])) if taille not in tuple_verif else None

			liste_taille[i] = int(liste_taille[i])
			liste_decoupe_mot[i] = configurer_decoupage(option, nom_option, liste_decoupe_mot[i], liste_generation[i], intervalle_debut, taille, tuple_verif) if liste_decoupe_mot[i] != None else None

			for j in range(len(liste_mot[i])):
				if verifier_dictionnaire(liste_mot[i][liste_nb_mot[i]]) == True:
					intervalle = liste_mot[i][liste_nb_mot[i]][liste_mot[i][liste_nb_mot[i]].index("[") + 1:-1]
					liste_mot[i][liste_nb_mot[i]] = liste_mot[i][liste_nb_mot[i]][:liste_mot[i][liste_nb_mot[i]].index("[")]

					if (liste_type[i] == "f" and ":" in intervalle) or (liste_type[i] == "f" and intervalle == "0"):
						commande_erreur(nom_option + " " + option, len(nom_option) + 1 + intervalle_debut + (len(liste_generation[i]) - (len(str(liste_taille[i])) + 2 + len(intervalle))), len(nom_option) + 1 + intervalle_debut + (len(liste_generation[i]) - (len(str(liste_taille[i])) + 2)))

					liste_element_fichier, nb_element_fichier = conversion_dictionnaire(nom_option_precision, tuple_verif, liste_generation[i], liste_mot[i][liste_nb_mot[i]], intervalle)
					liste_nb_mot[i] += nb_element_fichier
					liste_mot[i] = liste_mot[i][:liste_nb_mot[i] - (nb_element_fichier)] + liste_element_fichier + liste_mot[i][(liste_nb_mot[i] - nb_element_fichier) + 1:]
				else:
					liste_nb_mot[i] += 1

			if (liste_type[i] == 'f' and liste_nb_mot[i] != 1) or (liste_type[i] in ['a', 'p', 'c', 'C'] and liste_nb_mot[i] < 2):
				commande_erreur(nom_option_precision[:2] + " " + option, len(nom_option_precision[:2]) + 1 + intervalle_debut + 2, len(nom_option_precision[:2]) + 1 + intervalle_debut + 2 + len("".join(liste_mot[i])) + len(liste_mot[i]) - 1)

			intervalle_debut += len(liste_generation[i]) + 1

		return liste_type, liste_mot, liste_nb_mot, liste_taille, liste_decoupe_mot


	def configurer_intervalle(nom_option, generation, dictionnaire, tuple_verif, chaine, intervalle_max):
		if chaine.count(":") == 0:
			liste_intervalle = [chaine]
		elif chaine.count(":") == 1:
			liste_intervalle = chaine.split(":")
		elif chaine.count(":") > 1:
			commande_erreur(nom_option + " " + generation, len(nom_option) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1 - (len(chaine) + 2), len(nom_option) + 1 + generation.index(dictionnaire) + len(dictionnaire) - 1)

		for i in range(len(liste_intervalle)):
			if liste_intervalle[i] != '':
				for car in liste_intervalle[i]:
					if car not in tuple_verif:
						commande_erreur(nom_option[:2] + " " + generation, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1 + len(chaine))

		if len(liste_intervalle) == 1:
			liste_intervalle = [int(liste_intervalle[0])]
		elif liste_intervalle[0] == '' and liste_intervalle[1] == '':
			if intervalle_max == 1:
				liste_intervalle = [1]
			else:
				liste_intervalle = [1, intervalle_max]
		elif liste_intervalle[0] == '' and liste_intervalle[1] != '':
			liste_intervalle = [1, int(liste_intervalle[1])]
		elif liste_intervalle[0] != '' and liste_intervalle[1] == '':
			liste_intervalle = [int(liste_intervalle[0]), intervalle_max]
		elif liste_intervalle[0] != '' and liste_intervalle[1] != '' and int(liste_intervalle[0]) < int(liste_intervalle[1]):
			liste_intervalle = [int(liste_intervalle[0]), int(liste_intervalle[1])]
		elif liste_intervalle[0] != '' and liste_intervalle[1] != '' and int(liste_intervalle[0]) > int(liste_intervalle[1]):
			liste_intervalle = [int(liste_intervalle[0]), int(liste_intervalle[1])]
		elif liste_intervalle[0] != '' and liste_intervalle[1] != '' and int(liste_intervalle[0]) == int(liste_intervalle[1]):
			commande_erreur(nom_option[:2] + " " + generation, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1 + len(chaine))

		for i in range(len(liste_intervalle)):

			if liste_intervalle[i] > intervalle_max or liste_intervalle[i] < 1:
					commande_erreur(nom_option[:2] + " " + generation, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1, len(nom_option[:2]) + 1 + generation.index(dictionnaire) + len(dictionnaire) + 1 + len(chaine))

		return liste_intervalle


	def configurer_decoupage(option, nom_option, chaine, generation, intervalle_debut, taille, tuple_verif):
		liste_decoupe = None

		if chaine == "/":
			commande_erreur(nom_option + " " + option, len(nom_option) + 1 + (len(option) - 1), len(nom_option) + 1 + len(option))
		else:

			if chaine[0] == "/":
				liste_decoupe = analyser_separation(nom_option, 0, chaine[1:], "/", 0)
				compteur_decoupage = 0

				for i in range(len(liste_decoupe)):
					for j in range(len(liste_decoupe[i])):
						if liste_decoupe[i][j] not in tuple_verif:
							commande_erreur(nom_option + " " + generation, len(nom_option) + 1 + len(generation) - len(chaine[1:]), len(nom_option) + 1 + len(generation))

						compteur_decoupage += len(liste_decoupe[i]) + 1

				liste_decoupe = list(map(int, liste_decoupe))

				for i in range(len(liste_decoupe)):
					if int(liste_decoupe[i]) > int(taille):
						commande_erreur(nom_option + " " + chaine, len(nom_option) + 1 + chaine.index("/" + str(liste_decoupe[i])) + 1, len(nom_option) + 1 + chaine.index("/" + str(liste_decoupe[i])) + len(str(liste_decoupe[i])) + 1)

		return liste_decoupe


	def conversion_dictionnaire(nom_option_precision, tuple_verif, liste_generation, nom_dictionnaire, intervalle):
		liste_element_fichier = verifier_existence_fichier(nom_dictionnaire, True)
		intervalle = configurer_intervalle(nom_option_precision, liste_generation, nom_dictionnaire, tuple_verif, intervalle, len(liste_element_fichier))

		if len(intervalle) == 1:
			return supprimer_retour_ligne([liste_element_fichier[intervalle[0] - 1]]), 1
		elif len(intervalle) == 2:
			if intervalle[0] < intervalle[1]:
				return supprimer_retour_ligne(liste_element_fichier[intervalle[0] - 1:intervalle[1]]), (intervalle[1] - intervalle[0]) + 1
			elif intervalle[0] > intervalle[1]:
				return supprimer_retour_ligne(list(reversed(liste_element_fichier[intervalle[1] - 1:intervalle[0]]))), (intervalle[0] - intervalle[1]) + 1


	def analyser_separation(nom_option, commande_debut, chaine, separation, nb_debut):
		if chaine[0] == separation:
			commande_erreur(nom_option + " " + chaine, len(nom_option) + 1 + commande_debut + nb_debut, len(nom_option) + 1 + commande_debut + nb_debut + 1)
		elif chaine[-1] == separation:
			commande_erreur(nom_option + " " + chaine, len(nom_option) + 1 + commande_debut + nb_debut + len(chaine[commande_debut + nb_debut:]) - 1, len(nom_option) + 1 + commande_debut + nb_debut + len(chaine[commande_debut + nb_debut:]))
		elif (separation * 2) in chaine:
			commande_erreur(nom_option + " " + chaine, len(nom_option) + 1 + commande_debut + nb_debut + chaine[commande_debut + nb_debut:].index(separation * 2), len(nom_option) + 1 + commande_debut + nb_debut + chaine[commande_debut + nb_debut:].index(separation * 2) + 2)

		return chaine[commande_debut + nb_debut:].split(separation)


	def verifier_dictionnaire(dictionnaire):
		if dictionnaire.count("[") == 1 and dictionnaire.count("]") == 1 and dictionnaire[-1] == "]":
			return True
		else:
			return False


	def estimer(option, nom_option, liste_type, liste_nb_mot, liste_taille):
		liste_estimation = []
		intervalle_debut = 0
		liste_generation = option.split("+")

		for i in range(len(liste_type)):
			if (liste_type[i] == 'p' or liste_type[i] == 'c') and liste_nb_mot[i] < liste_taille[i]:
				commande_erreur(nom_option + " " + option, len(nom_option) + 1 + intervalle_debut + len(liste_generation[i]) - len(liste_generation[i].split(",")[-1]), len(nom_option) + 1 + intervalle_debut + len(liste_generation[i]))
			elif liste_type[i] == 'f':
				liste_estimation.append(None)
			elif liste_type[i] == 'a':
				liste_estimation.append(Estimer.arrangement(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'p':
				liste_estimation.append(Estimer.permutation(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'C':
				liste_estimation.append(Estimer.Combinaison(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'c':
				liste_estimation.append(Estimer.combinaison(liste_nb_mot[i], liste_taille[i]))

			intervalle_debut += len(liste_generation[i]) + 1

		return liste_estimation

except KeyboardInterrupt:
	print("\033[0m" + "\n")
