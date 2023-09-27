### par Grégory SCHAAF ###

from copy import deepcopy
import hashlib
import os
import sys
import time

from dnb import *
from global_fonc import (
	centrer,
	commande_erreur,
	configurer_generation,
	estimer,
	legal,
	supprimer_retour_ligne,
	verifier_existence_fichier,
	verifier_permission
	)


try:

	def argument():
		liste_argument = sys.argv
		liste_option = ('r', '-t', '-c')
		option_r = None
		option_t = None
		option_c = None

		for i in range(len(liste_argument)):
			if liste_argument[i] == '-r' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_r = liste_argument[i + 1]
			elif liste_argument[i] == '-t' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_t = liste_argument[i + 1]
			elif liste_argument[i] == '-c' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_c = liste_argument[i + 1]

		if option_c == None:
			commande_erreur("-c", 0, 2)

		return option_r, option_t, option_c


	def intro_ignis():
		largeur = centrer(24, None)
		print("\033[0m" + "\033[1m" + "\033[96m" + " " * largeur[0] +
""" __ ____ _      __ ____\n""" + " " * largeur[0] +
"""Γ |Γ  _/Γ ||Ξ||Γ |Γ _Ξ/\n""" + " " * largeur[0] +
"""| || |_|| \\\\ ||| ||__ |\n""" + " " * largeur[0] +
"""ιΞ|ι___||_|ι_||ιΞ|ιΞ__/\n""" +
"\033[0m" + " " * centrer(14, None)[0] + "\033[3m" + "\033[34m" + "Grégory SCHAAF" + "\033[0m" + "\n\n")


	def barre_pourcentage(compteur_test, estimation, surlignage):
		largeur_barre = int((os.get_terminal_size()[0] * 70) / 100)
		taux_visuel = str((compteur_test * 100) / estimation)

		if "e" in str(taux_visuel):
			taux_visuel = "0.00"
		else:
			taux_visuel = taux_visuel[:taux_visuel.index(".") + 3]

		taux_visuel += "%"
		pourcent_barre = compteur_test * largeur_barre / estimation
		liste_element_barre = centrer(len(taux_visuel + "%"), largeur_barre)
		barre = (" " * liste_element_barre[0]) + taux_visuel + (" " * liste_element_barre[1])
		return (" " * centrer(len(barre), None)[0]) + surlignage + barre[:int(pourcent_barre)] + "\033[100m" + barre[int(pourcent_barre):] + "\033[0m"


	def rendu_parametrage(visuel, nb_affichage, auth, estimation):
		rendu = "\033[0m" + "\033[1m" + "\033[37m" + str(nb_affichage) + "   " + str(estimation) + "   " + auth + "\033[0m"
		largeur = centrer(6 + len(str(estimation)) + len(auth) + len(str(nb_affichage)), None)
		print((" " * largeur[0]) + rendu + (" " * largeur[1]) + "\033[0m")
		print("\n")
		print("\n")
		print('\n')


	def rendu_authentification(visuel, utilisateur, mdp, estimation, bool_auth, precedente_largeur, nb_affichage, auth, compteur_affichage, compteur_test):
		if bool_auth == True:
			couleur_texte = "\033[36m"
			surlignage = "\033[46m"
		else:
			couleur_texte = "\033[35m"
			surlignage = "\033[45m"

		if visuel == "%":
			if os.get_terminal_size()[0] != precedente_largeur:
				os.system("clear")
				os.system("clear")

				intro_ignis()
				rendu_parametrage(visuel, nb_affichage, auth, estimation)

			rendu = "\033[0m" + couleur_texte + str(compteur_affichage) + "\033[0m" + " "
			nb_rendu = len(str(compteur_affichage)) + 1
			barre = barre_pourcentage(compteur_test, estimation, surlignage)

			if utilisateur != None:
				rendu += couleur_texte + "\033[3m" + "\033[1m" + utilisateur + "\033[0m" + " "
				nb_rendu += len(utilisateur) + 1

			if mdp != None:
				rendu += couleur_texte + "\033[3m" + "\033[1m" + mdp + " "
				nb_rendu += len(mdp) + 1

			rendu += "\033[0m" + couleur_texte + str(compteur_test) + "\033[0m"
			nb_rendu += len(str(compteur_test))

			largeur_terminal = centrer(nb_rendu, None)
			rendu = (" " * largeur_terminal[0]) + rendu + (" " * largeur_terminal[1])

			for i in range(3):
				sys.stdout.write("\033[F")

			print(rendu + "\n" + barre + "\n")

		elif visuel == "/":
			rendu = "\033[0m" + couleur_texte + str(compteur_affichage) + "\033[0m" + " "
			nb_rendu = len(str(compteur_affichage)) + 1

			if utilisateur != None:
				rendu += couleur_texte + "\033[3m" + "\033[1m" + utilisateur + "\033[0m" + " "
				nb_rendu += len(utilisateur) + 1

			if mdp != None:
				rendu += couleur_texte + "\033[3m" + "\033[1m" + mdp + "\033[0m" + " "
				nb_rendu += len(mdp) + 1

			rendu += couleur_texte + str(compteur_test) + "\033[0m"
			nb_rendu += len(str(compteur_test))

			centrer_resultat = centrer(nb_rendu, None)
			print((" " * centrer_resultat[0]) + rendu)

		return os.get_terminal_size()[0]


	def verifier_repertoire(option_c):
		liste_config = [None, None, None]

		try:
			liste_contenu = os.listdir(option_c)
		except:
			commande_erreur("-c " + option_c, 3, 3 + len(option_c))

		if 'result.txt' not in liste_contenu or 'config' not in liste_contenu:
			commande_erreur("-c " + option_c, 3, 3 + len(option_c))

		r = open(option_c + "/config", "r")
		liste_config_recup = r.readlines()
		liste_config_recup = supprimer_retour_ligne(liste_config_recup)

		for config in liste_config_recup:
			index_config = None

			if len(config) > 2:
				if config[:2] == "a:":
					index_config = 0
				elif config[:2] == "u:":
					index_config = 1
				elif config[:2] == "p:":
					index_config = 2

				if index_config != None:
					liste_config[index_config] = config[2:]			

		if liste_config[0] == None:
			commande_erreur(option_c + "/config -a", len(option_c) + 8, len(option_c) + 10)
		if liste_config[1] == None:
			commande_erreur(option_c + "/config -u", len(option_c) + 8, len(option_c) + 10)
		if liste_config[2] == None:
			commande_erreur(option_c + "/config -p", len(option_c) + 8, len(option_c) + 10)
		return liste_config[0], liste_config[1], liste_config[2]


	def estimer_minimum(liste_estimation):
		if liste_estimation.count(None) == len(liste_estimation):
			return None
		else:
			for i in range(liste_estimation.count(None)):
				del liste_estimation[liste_estimation.index(None)]

			return min(liste_estimation)


	def estimer_minimum_final(liste_estimation_gen_max):
		if liste_estimation_gen_max == [None, None]:
			return 1
		elif None in liste_estimation_gen_max:
			del liste_estimation_gen_max[liste_estimation_gen_max.index(None)]
		
		return min(liste_estimation_gen_max)


	def configurer_temps(option_t, liste_verif):
		if option_t.count(".") > 1:
			commande_erreur("-t " + option_t, 3, 3 + len(option_t))

		for i in range(len(option_t)):
			if option_t[i] not in liste_verif:
				commande_erreur("-t " + option_t, 3, 3 + len(option_t))

		return float(option_t)


	def configurer_rendu(option, nom_option, estimation_max):
		liste_affichage = ['/', '%']

		if option == None:
			type_affichage = random.choice(liste_affichage)
			option = estimation_max
		elif option in liste_affichage:
			type_affichage = option
			option = estimation_max

		else:
			if option[0] in liste_affichage:
				type_affichage = option[0]
				option = option[1:]
			else:
				type_affichage = random.choice(liste_affichage)

			if option == '':
				commande_erreur(nom_option + " " + option, len(nom_option) + 1, len(nom_option) + 1 + len(option))

			for i in range(len(option)):
				if option[i] not in list(map(str, list(range(0, 9)))):
					commande_erreur(nom_option + " " + option, len(nom_option) + 1, len(nom_option) + 1 + len(option))

		return type_affichage, int(option)


	def configurer_modele(liste_type, liste_nb_mot, liste_taille):
		liste_modele = []

		for i in range(len(liste_type)):
			if liste_type[i] == 'f':
				liste_modele.append(None)
			elif liste_type[i] == 'a':
				liste_modele.append(Modeliser.arrangement(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'p':
				liste_modele.append(Modeliser.permutation(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'C':
				liste_modele.append(Modeliser.Combinaison(liste_nb_mot[i], liste_taille[i]))
			elif liste_type[i] == 'c':
				liste_modele.append(Modeliser.combinaison(liste_nb_mot[i], liste_taille[i]))

		return liste_modele


	def decouper(liste_resultat, liste_decoupe):
		liste = []

		for i in range(len(liste_decoupe)):
			liste.append(liste_resultat[liste_decoupe[i] - 1])

		return liste


	def generer(type_mot, liste_mot, liste_taille, modele, ordre):
		liste_resultat = []

		if type_mot in ('a', 'p', 'C', 'c'):
			if type_mot == 'a':
				liste_resultat = Convertir.Liste.arrangement(modele, ordre - 1)
			elif type_mot == 'p':
				liste_resultat = Convertir.Liste.permutation(modele, ordre - 1)
			elif type_mot == 'C':
				liste_resultat = Convertir.Liste.Combinaison(modele, ordre - 1)
			elif type_mot == 'c':
				liste_resultat = Convertir.Liste.combinaison(modele, ordre - 1)

			for i in range(liste_taille):
				liste_resultat[i] = (liste_mot[liste_resultat[i]])

		elif type_mot == 'f':
			for i in range(liste_taille):
				liste_resultat.append(liste_mot[0])

		return liste_resultat


	def tester(auth, liste_dictionnaire, utilisateur, mdp):
		if auth == None:
			return False
		elif auth in ('blake2b', 'sha3_256', 'sha3_224', 'sha3_384', 'sha512', 'sha384', 'blake2s', 'sha1', 'sha224', 'sha256', 'md5', 'sha3_512'):
			if auth == 'md5':
			    mdp_hash = hashlib.md5((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha1':
				mdp_hash = hashlib.sha1((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha224':
				mdp_hash = hashlib.sha224((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha256':
				mdp_hash = hashlib.sha256((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha384':
				mdp_hash = hashlib.sha384((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha512':
				mdp_hash = hashlib.sha512((mdp).encode("utf-8")).hexdigest()
			elif auth == 'blake2b':
				mdp_hash = hashlib.blake2b((mdp).encode("utf-8")).hexdigest()
			elif auth == 'blake2s':
				mdp_hash = hashlib.blake2s((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha3_224':
				mdp_hash = hashlib.sha3_224((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha3_256':
				mdp_hash = hashlib.sha3_256((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha3_384':
				mdp_hash = hashlib.sha3_384((mdp).encode("utf-8")).hexdigest()
			elif auth == 'sha3_512':
				mdp_hash = hashlib.sha3_512((mdp).encode("utf-8")).hexdigest()

			if utilisateur == mdp_hash:
				return True

			return False

		elif auth == "dico":
			try:
				a = open(utilisateur, "a")
				a.write(liste_dictionnaire)
				a.close()
				return False
			except FileNotFoundError:
				exit()

		else:
			commande_erreur("-a " + auth, 3, 3 + len(auth))


	def ajuster_progression_liste_gen(chemin_fichier, liste_gen, estimation_gen_max):
		type_gen = type(liste_gen[0][liste_gen[2]])

		if type_gen == list:
			if liste_gen[0][liste_gen[2]][0] < liste_gen[0][liste_gen[2]][1]:
				type_gen = True
			elif liste_gen[0][liste_gen[2]][0] > liste_gen[0][liste_gen[2]][1]:
				type_gen = False

		if liste_gen[2] == len(liste_gen[0]) - 1:
			if type_gen == int or (liste_gen[1] == liste_gen[0][liste_gen[2]][1]):
				if liste_gen[3] == liste_gen[4]:
					return True

				liste_gen[3] += 1
				return compter_fichier(chemin_fichier, liste_gen[3], estimation_gen_max)

		if type_gen == int or liste_gen[1] == liste_gen[0][liste_gen[2]][1]:
			if type(liste_gen[0][liste_gen[2] + 1]) == int:
				liste_gen[2] += 1
				liste_gen[1] = liste_gen[0][liste_gen[2]]
			elif type(liste_gen[0][liste_gen[2] + 1]) == list and liste_gen[0][liste_gen[2] + 1][0] < liste_gen[0][liste_gen[2] + 1][1]:
				liste_gen[2] += 1
				liste_gen[1] = liste_gen[0][liste_gen[2]][0]
			elif type(liste_gen[0][liste_gen[2] + 1]) == list and liste_gen[0][liste_gen[2] + 1][0] > liste_gen[0][liste_gen[2] + 1][1]:
				liste_gen[2] += 1
				liste_gen[1] = liste_gen[0][liste_gen[2]][0]
		else:
			if type(liste_gen[0][liste_gen[2]]) == list and liste_gen[0][liste_gen[2]][0] < liste_gen[0][liste_gen[2]][1] and liste_gen[1] != liste_gen[0][liste_gen[2]][1]:
				liste_gen[1] += 1
			elif type(liste_gen[0][liste_gen[2]]) == list and liste_gen[0][liste_gen[2]][0] > liste_gen[0][liste_gen[2]][1] and liste_gen[1] != liste_gen[0][liste_gen[2]][1]:
				liste_gen[1] -= 1

		return liste_gen


	def compter_fichier(chemin_fichier, ligne_recup, estimation):
		liste_finale_element = []
		compteur_ligne = 0
		compteur_gen = 0

		for ligne in open(chemin_fichier, 'r'):
			compteur_ligne += 1
			ligne = ligne[:-1] if ligne[-1] == "\n" else ligne
			liste_ligne = ligne.split(",")

			for i in range(len(liste_ligne)):
				element = liste_ligne[i].split(":")

				for j in range(len(element)):
					try:
						element[j] = int(element[j])
					except ValueError:
						commande_erreur(chemin_fichier + " -> l" + str(compteur_ligne) + ":" + str(i + 1), len(chemin_fichier) + 4, len(chemin_fichier) + 5 + len(str(compteur_ligne)) + 1 + len(str(i + 1)))
					except KeyboardInterrupt:
						print("\033[0m" + "\n")

					if element[j] > estimation:
						commande_erreur(chemin_fichier + " -> l" + str(compteur_ligne) + ":" + str(i + 1), len(chemin_fichier) + 4, len(chemin_fichier) + 5 + len(str(compteur_ligne)) + 1 + len(str(i + 1)))

				if len(element) == 1:
					compteur_gen += 1
					liste_ligne[i] = element[j]
				elif len(element) == 2:
					if element[0] < element[1]:
						compteur_gen += (element[1] - element[0]) + 1
					elif element[0] > element[1]:
						compteur_gen += (element[0] - element[1]) + 1
					else:
						compteur_gen += 1

					liste_ligne[i] = element
				else:
					commande_erreur(chemin_fichier + " -> l" + str(compteur_ligne) + ":" + str(i + 1), len(chemin_fichier) + 4, len(chemin_fichier) + 5 + len(str(compteur_ligne)) + 1 + len(str(i + 1)))

			if compteur_ligne == ligne_recup:
				liste_finale_element = liste_ligne

		if compteur_ligne == 0:
			commande_erreur(chemin_fichier, 0, len(chemin_fichier))
			exit()

		if type(liste_finale_element[0]) == int:
			progres_element = liste_finale_element[0]
		else:
			progres_element = liste_finale_element[0][0]

		return [liste_finale_element, progres_element, 0, 1, compteur_ligne, compteur_gen]


	def analyser_fichier_gen(nom_rep, liste_nb_gen, liste_estimation):
			liste_gen = [None, None]

			if 'u' in os.listdir(nom_rep):
				liste_gen[0] = []
			if 'p' in os.listdir(nom_rep):
				liste_gen[1] = []

			for i in range(2):
				if liste_nb_gen[i] != None:
					if i == 0 and liste_gen[0] == []:
						rep = "u/"
					elif i == 1 and liste_gen[1] == []:
						rep = "p/"

					for j in range(liste_nb_gen[i]):
						chemin_fichier = nom_rep + rep + str(j + 1) + ".g"
						verifier_existence_fichier(chemin_fichier, False)

						if liste_estimation[i][j] == None:
							estimation = 1
						else:
							estimation = liste_estimation[i][j]

						liste_gen[i].append(compter_fichier(chemin_fichier, 1, estimation))

			return liste_gen


	def main():
		os.system("clear")
		intro_ignis()
		verifier_permission()
		legal("ignis")
		option_r, option_t, option_c = argument()
		option_a, option_u, option_p = verifier_repertoire(option_c)

		if option_u == None and option_p == None:
			exit()

		temps = None
		tuple_verif_09 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.')
		liste_nb_mot = [None, None]
		liste_nb_gen = [None, None]
		liste_dictionnaire = ""
		liste_mot = [option_u, option_p]
		liste_resultat = [None, None]
		liste_taille = [None, None]
		liste_type = [None, None]
		liste_decoupe = [None, None]
		liste_estimation = [[], []]
		liste_estimation_gen_max = [None, None]
		liste_modele = [None, None]
		status_recherche = False

		if option_a == "dico":
			contenu_dictionnaire = ""

		if option_t != None:
			temps = configurer_temps(option_t, tuple_verif_09)

		for i in range(2):
			if liste_mot[i] != None:
				if i == 0:
					option = option_u
					existence = "u"
				elif i == 1:
					option = option_p
					existence = "p"

				liste_type[i], liste_mot[i], liste_nb_mot[i], liste_taille[i], liste_decoupe[i] = configurer_generation(tuple_verif_09[:-1], option, "-" + existence)
				liste_nb_gen[i] = len(liste_type[i])
				liste_estimation[i] = estimer(option, "-" + existence, liste_type[i], liste_nb_mot[i], liste_taille[i])
				liste_modele[i] = configurer_modele(liste_type[i], liste_nb_mot[i], liste_taille[i])

		liste_gen = analyser_fichier_gen(option_c + "/", liste_nb_gen, liste_estimation)
		liste_estimation_brut = deepcopy(liste_estimation)

		for i in range(2):
			if liste_nb_gen[i] != None:
				for j in range(liste_nb_gen[i]):
					liste_estimation[i][j] = liste_gen[i][j][-1] if liste_type[i][j] != "f" else None

				liste_estimation_gen_max[i] = estimer_minimum(liste_estimation[i])

		estimation_max = estimer_minimum_final(liste_estimation_gen_max)
		type_affichage, nb_affichage = configurer_rendu(option_r, "-r", estimation_max)

		if estimation_max < nb_affichage:
			commande_erreur(str(nb_affichage) + " " + str(estimation_max), 0, len(str(nb_affichage)))

		affichage_init = estimation_max / nb_affichage
		affichage = int(affichage_init);
		compteur_affichage = 1
		rendu_parametrage(type_affichage, nb_affichage, option_a, estimation_max)
		precedente_largeur = os.get_terminal_size()[0]

		for compteur_general in range(estimation_max):
			for i in range(2):
				if liste_nb_gen[i] != None:
					liste_resultat[i] = [None] * len(liste_mot[i])

					for j in range(liste_nb_gen[i]):
						liste_resultat[i][j] = generer(liste_type[i][j], liste_mot[i][j], liste_taille[i][j], liste_modele[i][j], liste_gen[i][j][1])

						if liste_decoupe[i][j] != None:
							liste_resultat[i][j] = decouper(liste_resultat[i][j], liste_decoupe[i][j])

						liste_resultat[i][j] = "".join(liste_resultat[i][j])

					if type(liste_resultat[i]) == list:
						liste_resultat[i] = "".join(liste_resultat[i])

			if temps != None:
				time.sleep(temps)

			status_recherche = tester(option_a, liste_dictionnaire, liste_resultat[0], liste_resultat[1])
			liste_dictionnaire = ""

			if option_a == "dico":
				contenu_dictionnaire += liste_resultat[1] + "\n"

			if status_recherche == True:
				precedente_largeur = rendu_authentification(type_affichage, liste_resultat[0], liste_resultat[1], estimation_max, status_recherche, precedente_largeur, nb_affichage, option_a, compteur_affichage, compteur_general + 1)
				a = open(option_c + "/result.txt", "a")
				a.write(
				'[' + str(time.strftime('%d', time.localtime(time.time()))) + '-' +
				str(time.strftime('%m', time.localtime(time.time()))) + '-' +
				str(time.strftime('%Y', time.localtime(time.time()))) + '|' +
				str(time.strftime('%H', time.localtime(time.time()))) + ':' +
				str(time.strftime('%M', time.localtime(time.time()))) + ':' +
				str(time.strftime('%S', time.localtime(time.time()))) + '] ' +
				liste_resultat[0] + '/' + liste_resultat[1] + '/' +
				option_a + '/' + str(compteur_general) + '\n'
				)
				exit()

			if compteur_general + 1 == int(affichage):
				if option_a == "dico":
					a = open(liste_resultat[0], "a")
					a.write(contenu_dictionnaire)
					a.close()

					contenu_dictionnaire = ""

				precedente_largeur = rendu_authentification(type_affichage, liste_resultat[0], liste_resultat[1], estimation_max, status_recherche, precedente_largeur, nb_affichage, option_a, compteur_affichage, compteur_general + 1)
				compteur_affichage += 1

				if compteur_affichage == nb_affichage:
					affichage = estimation_max
				else:
					affichage += affichage_init

			for i in range(2):
				liste_option = ['u', 'p']

				for j in range(liste_nb_gen[i]):
					if liste_type[i][j] != "f":
						liste_gen[i][j] = ajuster_progression_liste_gen(option_c + "/" + liste_option[i] + "/" + str(j + 1) + ".g", liste_gen[i][j], liste_estimation_brut[i][j])

	main()

except KeyboardInterrupt:
	print("\033[0m" + "\n")
