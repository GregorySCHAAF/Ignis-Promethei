### par Grégory SCHAAF ###

import os
import random
import sys
import time

from global_fonc import (
	centrer,
	commande_erreur,
	configurer_generation,
	estimer,
	legal,
	verifier_permission
	)


try:

	def argument():
		liste_argument = sys.argv
		liste_option = ('-c', '-u', '-p', '-a')
		option_c = None
		option_u = None
		option_p = None
		option_a = None

		for i in range(len(liste_argument)):
			if liste_argument[i] == '-c' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_c = liste_argument[i + 1]
			elif liste_argument[i] == '-u' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_u = liste_argument[i + 1]
			elif liste_argument[i] == '-p' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_p = liste_argument[i + 1]
			elif liste_argument[i] == '-a' and i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
				option_a = liste_argument[i + 1]

				if i != len(liste_argument) - 1 and liste_argument[i + 1] not in liste_option:
					i += 1

		if option_u == None:
			commande_erreur("-u", 0, 2)
		elif option_p == None:
			commande_erreur("-p", 0, 2)

		return option_c, option_u, option_p, option_a


	def intro_promethei():
		largeur = centrer(47, None)
		print("\033[0m" + "\033[1m" + "\033[96m" + " " * largeur[0] +
""" ____ ____  __   _   _  _________ _  _  ____ __\n""" + " " * largeur[0] + 
"""Γ   /Γ   / Γ  \\ Γ \\ / |Γ___/\\   /Γ || |Γ___/Γ |\n""" + " " * largeur[0] +
"""||_/ | Ξ \\| Ξ  ||  Ξ  ||Ξ_|  | | | ΞΞ ||Ξ_| | |\n""" + " " * largeur[0] +
"""ιΞ|  ι_|Ξ| ι__ι ι_Ξ|Ξ_ιι___\\ ιΞ| ι_||Ξιι___\\ιΞ|\n""" +
"\033[0m" + " " * centrer(14, None)[0] + "\033[3m" + "\033[34m" + "Grégory SCHAAF" + "\033[0m" + "\n")


	def creer_sauvegarde(option_c, option_a, option_u, option_p, liste_type, liste_estimation):
		if option_a == None:
			option_a = "_"
		if option_u == None:
			option_u = "_"
		if option_p == None:
			option_p = "_"
		if option_c == None or os.path.exists(option_c):
			liste_repertoire = []
			option_c = "config_"

			for i in range(16):
				option_c += random.choice("0123456789")
		else:
			if "/" in option_c or "\\" in option_c:
				commande_erreur("-c " + option_c, 3, len(option_c) + 3)

		os.system("mkdir " + option_c)
		w = open(option_c + "/config", "w")
		w.write("a:" + option_a + "\nu:" + option_u + "\np:" + option_p + "\n")
		w.close()
		w = open(option_c + "/result.txt", "w")
		w.write("")
		w.close()

		for i in range(len(liste_type)):
			if liste_type[i] != None:
				if i == 0:
					gen = "u"
				else:
					gen = "p"

				os.system("mkdir " + option_c + "/" + gen)

				for j in range(len(liste_type[i])):
					w = open(option_c + "/" + gen + "/" + str(j + 1) + ".g", "w")

					if liste_type[i][j] == 'f':
						w.write("1")
					else:
						w.write("1:" + str(liste_estimation[i][j]))

					w.close()

		print("\033[1m" + "\033[44m" + " " + "\033[0m" + "\033[3m" + "\033[96m" + " " + option_c + "\033[0m" + "\n")


	def main():
		os.system("clear")
		intro_promethei()
		verifier_permission()
		legal("promethei")
		option_c, option_u, option_p, option_a = argument()

		if option_u == None and option_p == None:
			exit()

		tuple_verif_09 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.')
		liste_nb_mot = [None, None]
		liste_mot = [option_u, option_p]
		liste_taille = [None, None]
		liste_type = [None, None]
		liste_estimation = [[], []]
		vide = ""

		for i in range(2):
			if liste_mot[i] != None:
				if i == 0:
					option = option_u
					nom_option = "u"
				elif i == 1:
					option = option_p
					nom_option = "p"

				liste_type[i], vide, liste_nb_mot[i], liste_taille[i], vide = configurer_generation(tuple_verif_09[:-1], option, "-" + nom_option)
				liste_estimation[i] = estimer(option, "-" + nom_option, liste_type[i], liste_nb_mot[i], liste_taille[i])

		creer_sauvegarde(option_c, option_a, option_u, option_p, liste_type, liste_estimation)
		exit()

	main()

except KeyboardInterrupt:
	print("\033[0m" + "\n")
