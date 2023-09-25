### par Grégory SCHAAF ###

from copy import deepcopy
from math import factorial


class Suite:

	def __init__(self):
		pass


	def arrangement(cls, liste, nb_car):

		if None in liste:
			liste = [0] * len(liste)
		else:
			nb_car -= 1

			for i in range(len(liste) - 1, -1, -1):
				if liste[i] == nb_car:
					liste[i] = 0
				else:
					liste[i] += 1
					break

		return liste
		

	arrangement = classmethod(arrangement)


	def permutation(cls, liste, nb_car):

		if None in liste:
			liste = list(range(0, len(liste)))
		else:
			nb_liste = len(liste)

			for compte in range(nb_liste - 1, -1, -1):
				car = 1

				while liste[compte] + car != nb_car:
					if liste[compte] + car not in liste[:compte]:
						liste[compte] += car
						liste = liste[:compte + 1]
						i = 0

						while len(liste) != nb_liste:
							if liste.count(i) == 0:
								liste.append(i)
							i += 1

						return liste

					car += 1

		return liste

	permutation = classmethod(permutation)


	def Combinaison(cls, liste, nb_car):

		if None in liste:
			liste = [0] * len(liste)
		else:
			nb_liste = len(liste)

			if liste[-1] != nb_car - 1:
				liste[-1] += 1
			else:
				compte = nb_liste - 1

				while compte != 0:
					compte -= 1

					if liste[compte + 1] - liste[compte] >= 1:
						liste = liste[:compte] + ([liste[compte] + 1] * (len(liste[compte:])))
						break

		return liste

	Combinaison = classmethod(Combinaison)


	def combinaison(cls, liste, nb_car):

		if None in liste:
			liste = list(range(0, len(liste)))
		else:
			nb_liste = len(liste)

			if liste[-1] != nb_car - 1:
				liste[-1] += 1
			else:
				compte = nb_liste - 1

				while compte != 0:
					compte -= 1

					if liste[compte + 1] - liste[compte] >= 2:
						liste = liste[:compte] + list(range(liste[compte] + 1, liste[compte] + 1 + len(liste[compte:])))
						break

		return liste

	combinaison = classmethod(combinaison)


class Modeliser:

	def __init__(self):
		pass


	def arrangement(cls, nb_car, longueur):
		m = [1] * longueur

		for i in range(longueur - 2, -1, -1):
			m[i] = m[i + 1] * nb_car

		return m

	arrangement = classmethod(arrangement)


	def permutation(cls, nb_car, longueur):
		multiple = (nb_car - longueur) + 1
		m = [1] * longueur

		for i in range(longueur - 2, -1, -1):
			m[i] = m[i + 1] * multiple
			multiple += 1

		return m

	permutation = classmethod(permutation)


	def Combinaison(cls, nb_car, longueur):
		m = [[1] * nb_car]

		for i in range(1, longueur):
			m.append([])

			for j in range(nb_car):
				m[i].append(sum(m[i - 1][j:]))

		return m

	Combinaison = classmethod(Combinaison)


	def combinaison(cls, nb_car, longueur):
		m_valeur = []
		nb_car_max = (nb_car - longueur) + 1

		for i in range(nb_car_max):
			m_valeur.append([])

		car = 0

		for i in range(nb_car_max):
			m_valeur[i].append([[car]])
			car_duplication = car
			nb_bloc = 1

			for profondeur in range(1, longueur):
				m_valeur[i].append([])
				liste_duplication = []
				car_duplication += 1

				for compteur_duplication in range(nb_car_max):
					liste_duplication.append(car_duplication + compteur_duplication)

				if profondeur == 1:
					m_valeur[i][profondeur].append(liste_duplication)
				else:
					for bloc in range(len(m_valeur[i][profondeur - 1])):
						commencement_liste_duplication = len(liste_duplication) - len(m_valeur[i][profondeur - 1][bloc])

						for element in range(commencement_liste_duplication, commencement_liste_duplication + len(m_valeur[i][profondeur - 1][bloc])):
							m_valeur[i][profondeur].append(liste_duplication[element:])

			car += 1
			nb_car_max -= 1

		m_intervalle = deepcopy(m_valeur)
		intervalle = 0

		for i in range(len(m_intervalle)):
			for bloc in range(len(m_intervalle[i][-1])):
				for element in range(len(m_intervalle[i][-1][bloc])):
					m_intervalle[i][-1][bloc][element] = [intervalle]
					intervalle += 1

		for i in range(len(m_intervalle)):
			for profondeur in range(len(m_intervalle[i]) -2, -1, -1):
				compteur_bloc_2 = 0

				for compteur_bloc in range(len(m_intervalle[i][profondeur])):
					for compteur_element in range(len(m_intervalle[i][profondeur][compteur_bloc])):
						if m_intervalle[i][profondeur + 1][compteur_bloc_2][0][0] == m_intervalle[i][profondeur + 1][compteur_bloc_2][-1][-1]:
							m_intervalle[i][profondeur][compteur_bloc][compteur_element] = [m_intervalle[i][profondeur + 1][compteur_bloc_2][0][0]]
						else:
							m_intervalle[i][profondeur][compteur_bloc][compteur_element] = [m_intervalle[i][profondeur + 1][compteur_bloc_2][0][0], m_intervalle[i][profondeur + 1][compteur_bloc_2][-1][-1]]

						compteur_bloc_2 += 1

		return [m_valeur, m_intervalle]

	combinaison = classmethod(combinaison)


class Convertir:

	def __init__(self):
		pass


	class Liste:

		def __init__(self):
			pass


		def arrangement(cls, m, num):
			liste = []

			for i in range(len(m)):
				if m[i] <= num:
					liste.append(num // m[i])
					num -= liste[-1] * m[i]
				else:
					liste.append(0)

			return liste

		arrangement = classmethod(arrangement)


		def permutation(cls, m, num):
			liste_conversion = [0] * len(m)
			reste = num

			for i in range(len(m)):
				liste_conversion[i] = reste // m[i]
				reste -= liste_conversion[i] * m[i]

			liste = []

			for i in range(len(liste_conversion)):
				curseur = liste_conversion[i]

				for j in range(len(liste)):
					if sorted(liste)[j] <= curseur:
						curseur += 1

				liste.append(curseur)

			return liste

		permutation = classmethod(permutation)


		def Combinaison(cls, m, num):
			reste = num
			liste = []
			i = len(m) - 1
			j = 0

			while len(liste) != len(m):
				if m[i][j] <= reste:
					while True:
						reste -= m[i][j]
						j += 1

						if m[i][j] > reste:
							i -= 1
							break

					liste.append(j)
				else:
					liste.append(j)
					i -= 1

			return liste

		Combinaison = classmethod(Combinaison)


		def combinaison(cls, m, num):
			m_valeur = m[0]
			m_intervalle = m[1]
			liste = []
			bloc = 0

			for i in range(len(m_intervalle)):
				if num in m_intervalle[i][0][0][0] or num < m_intervalle[i][0][0][0][-1]:
					for profondeur in range(len(m_intervalle[i])):
						continuer_bloc = True

						while True:
							for element in range(len(m_intervalle[i][profondeur][bloc])):
								if num in m_intervalle[i][profondeur][bloc][element] or num < m_intervalle[i][profondeur][bloc][element][-1]:
									liste.append(m_valeur[i][profondeur][bloc][element])
									continuer_bloc = False
									break

							if continuer_bloc == False:
								break

							bloc += 1

					break

			return liste

		combinaison = classmethod(combinaison)


	class Num:

		def __init__(self):
			pass


		def arrangement(cls, m, liste):
			num = 0

			for i in range(len(liste)):
				num += liste[i] * m[i]

			return num

		arrangement = classmethod(arrangement)


		def permutation(cls, m, liste):
			num = 0
			liste_emplacement = []

			for i in range(len(liste)):
				liste_compare = liste[:liste.index(liste[i])]
				liste_compare = sorted(liste_compare)
				index_liste_compare = 0

				for compteur in range(len(liste_compare)):
					if liste_compare[index_liste_compare] > liste[i]:
						del liste_compare[index_liste_compare]
					else:
						index_liste_compare += 1

				liste_emplacement.append(liste[i] - len(liste_compare))

			for i in range(len(m)):
				num += m[i] * liste_emplacement[i]

			return num

		permutation = classmethod(permutation)


		def Combinaison(cls, m, liste):
			dernier_index = 0
			num = 0
			index_ensemble = 0

			for i in range(len(m) - 1, -1, -1):
				if liste[index_ensemble] != dernier_index:
					num += sum(m[i][dernier_index:liste[index_ensemble]])
					dernier_index = liste[index_ensemble]

				index_ensemble += 1

			return num

		Combinaison = classmethod(Combinaison)


		def combinaison(cls, m, liste):
			nb_bloc = 0

			for profondeur in range(1, len(liste)):
				index_element = m[0][liste[0]][profondeur][nb_bloc].index(liste[profondeur])
				intervalle_bloc_final_test = m[1][liste[0]][profondeur][nb_bloc][index_element]

				if len(intervalle_bloc_final_test) == 1:
					return intervalle_bloc_final_test[0]

				for j in range(nb_bloc):
					index_element += len(m[0][liste[0]][profondeur][j])

				nb_bloc = index_element

		combinaison = classmethod(combinaison)


class Estimer:

	def __init__(self):
			pass


	def arrangement(cls, nb_car, longueur):
		return nb_car ** longueur

	arrangement = classmethod(arrangement)


	def permutation(cls, nb_car, longueur):
		fact1 = factorial(nb_car)

		if nb_car == longueur:
			return fact1
		elif nb_car > longueur and nb_car - longueur > 1:
			fact2 = factorial(nb_car - longueur)
			return fact1 // fact2
		elif nb_car > longueur and nb_car - longueur == 1:
			return fact1
		elif nb_car < longueur:
			return False

	permutation = classmethod(permutation)


	def Combinaison(cls, nb_car, longueur):
		return int(factorial((nb_car + longueur) - 1) / (factorial(longueur) * factorial(nb_car - 1)))

	Combinaison = classmethod(Combinaison)


	def combinaison(cls, nb_car, longueur):
		if nb_car > longueur:
			return int(factorial(nb_car) / (factorial(longueur) * factorial(nb_car - longueur)))
		elif nb_car == longueur:
			return 1
		else:
			return False

	combinaison = classmethod(combinaison)
