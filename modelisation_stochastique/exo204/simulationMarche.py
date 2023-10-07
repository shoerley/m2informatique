import numpy as np


def simulate_markov_chain(transition_matrix, initial_state, final_state, num_steps, num_simulations):
	"""
	Simule des marches aléatoires dans un graphe dont la matrice de transition est passée en paramètre.
	Renvoie la probabilité d'atteindre un état final à partir d'un état initial état donnée la longueur
	d'une marche aléatoire.

	Consignes :
		* Prendre le code en main, le tester en faisant varier les paramètres
		* Implémenter la matrice de transition de l'exercice 204 et tester le code avec
		* Retrouver la probabilité de passage trouvée à la question 204.4
		* Implémenter la matrice de transition de l'exercice 203 et tester le code avec
		* Retrouver les probabilités calculées aux questions 203.4 et 203.5
	:param transition_matrix: une matrice de transition
	:param initial_state: l'indice (à partir de 1) de l'état initial
	:param final_state: l'indice (à partir de 1) de l'état final
	:param num_steps: longueur (maximale) de la marche
	:param num_simulations: nombre de simulations
	:return: probabilité d'atteindre l'état final à partir de l'état initial en une marche de longueur donnée
	"""
	num_states = transition_matrix.shape[0]
	num_successes = 0

	for _ in range(num_simulations):
		current_state = initial_state
		reached_final_state = False

		for _ in range(num_steps):
			# Simulate the next state transition
			next_state = np.random.choice(num_states, p=transition_matrix[current_state])

			if next_state == final_state:
				reached_final_state = True
				break

			current_state = next_state

		if reached_final_state:
			num_successes += 1

	probability = num_successes / num_simulations
	return probability


# Exemple d'utilisation
transition_matrix_toy = np.array([[0.2, 0.8], [0.4, 0.6]])

initial_state = 1  # État initial
final_state = 2  # État final
num_steps = 10  # Nombre de sauts dans la marche
num_simulations = 10000  # Nombre de simulations

probability = simulate_markov_chain(transition_matrix_toy, initial_state-1, final_state-1, num_steps, num_simulations)

print(f"Probabilité d'atteindre l'état {final_state} à partir de l'état {initial_state} en {num_steps} sauts : {probability}")
