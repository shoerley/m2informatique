@author scholet @date november 2023

Ci-dessous des pistes pour la résolution d'un sélection d'exercices du TP de Cryptographie


## Codage de Vigenère

### 4. Ecrire une fonction longueurCle qui prend en paramètres le texte crypté t et qui retourne la longueur k probable de la clé de codage.

On utilise la fonction précédente pour créer une liste de tous les pgcd des distances entre les répétitions des séquences t[i], t[i+1], t[i+2] pour i allant de 0 à n – 6 où n est la longueur de t. Puis, on calcule le pgcd de tous les éléments de cette liste.

```python
	def longueurCle (t) :
		n = len(t)
		L = [pgcdDistancesEntreRepetitions(t,i) for i in range(n-5)]
		d = 0
		for k in L :
		if k != 0 :
		d = pgcd(k,d)
		return d
```

### 5. Donner le nombre maximal d’opérations réalisées par la fonction longueurCle en fonction de la longueur de t. On ne comptera que le nombre d’appels à la fonction pgcd.

On commence par compter le nombre d’appels à la fonction pgcd lors de l’exécution de `pgcdDistancesEntreRepetitions`. Dans le pire des cas, il y a un appel à chaque passage dans la boucle for, ce qui totalise `n-i-1` appels.
Ensuite, pour construire la liste `L` dans la fonction longueurCle, les `n-5` appels à `pgcdDistancesEntreRepetitions` engendrent en plus : 

```
	Somme (de i = 0 à i=n-6) de n-i-1 
		=	(n-1)(n-5) - ((n-6)(n-5))/2

```

appels à pgcd.
S’y ajoutent au pire (`k != 0`) autant d’appels direct à pgcd qu’il y a d’éléments dans `L`, c’est-à-dire `n-5`. Par conséquent, le nombre d’appels total à pgcd est au plus égal à : `((n-5)(n+6))/2`
Il s’agit d’une complexité quadratique, cet algorithme n’est pas très efficace.

### 6. Une fois la longueur de la clé connue, donnez une idée d’algorithme permettant de retrouver chacune des lettres de la clé. Il s’agit de décrire rapidement l’algorithme et non d’écrire le programme.

Une fois la longueur de la clé connue, on peut faire du décodage de César automatique sur les parties de textes codées par la même lettre (pour la jème lettre, les lettres d’indice `j-1,k+j-1,2k+j-1,...`). On détermine ainsi les lettres de la clé par analyse des fréquences puis on décode.

### 7. Question bonus. Ecrire une fonction decodageVigenereAuto qui prend en paramètres le texte crypté t et qui retourne le texte original probable.

On utilise deux fonctions : une première qui permet de retrouver la clé et une seconde fonction qui décode.

```python
	def estimerCle (t) :
		k = longueurCle(t)
		cle = [0 for j in range(k)]
		q = len(t) // k
		# on crée un tableau M contenant le texte de sorte que les éléments d’une
		# même colonne soient codés avec le même décalage
		M = np.zeros((q+1,k))
		for i in range(q) :
			M[i,:] = [t[i*k+j] for j in range(k)]
		M[q,0:len(t)-q*k] = [t[q*k+j] for j in range(len(t)-q*k]
		for j in range(k) :
			# on determine la lettre de la colonne j de la clé
			L = frequenceLettres(list(M[:q,j]))
			m, max = 0, L[0]
			for i in range(1,len(L)) :
				if L[i] > max :
					m, max = i, L[i]
			cle[j] = (m-4) % 26
		return cle

	def decodageVigenereAuto (t) :
		c = estimerCle(t)
		n, k = len(t), len(c)
		return [(t[i]-c[i%k]) % 26 for i in range(n)]
```


## Codage RSA

### 1.5. Ecrire une fonction `expoModulaire` qui calcule `a^n % m` lorsque `a`, `n` et `m` sont passés en paramètres. Vous écrirez cette fonction de manière récursive et en vous assurant que le nombre de multiplications effectuées est de l’ordre de `log2*n` (et non de `n`).

```python
def expoModulaire (a,n,m) :
	if n == 0 :
		return 1
	if n % 2 == 0 :
		return (expoModulaire(a,n//2,m)**2) % m
	return (a * expoModulaire(a,n//2,m)**2) % m

```


### 2.1 Ecrire une fonction `choixCle` de paramètres deux nombres `inf` et `lg`, permettant de créer un triplet `(p,q,e)` tel que `p` et `q` sont deux nombres premiers distincts où `𝑝∈[𝑖𝑛𝑓,𝑖𝑛𝑓+𝑙𝑔]` et `𝑞∈[𝑝+1,𝑝+𝑙𝑔+1]`, et `e` compris entre 2 et `(p-1)(q-1)` et `e` est premier avec `(p-1)(q-1)`.

Pour cette question, il faut remarquer que `p` est un nombre premier aléatoire entre deux bornes, tout comme `q`, à l'exception que `q = p+1`. Enfin, `e` est premier avec le produit `(p-1)(q-1)`. Dès lors, il suffit de faire les bons appels à `premierAléatoire` et `premierAléatoireAvec`.

### 2.2 Ecrire une fonction `clePublique` permettant de calculer la clé publique `(n,e)` à partir de `(p,q,e)` et une fonction `clePrivee` permettant de calculer la clé privée `(n,d)` à partir de `(p,q,e)`.


Il faut se servir de la relation `𝑛=𝑝×𝑞` et de l’inverse modulaire de `e` et `phi(n)`.


### 2.3 Ecrire une fonction `codageRSA` qui prend en paramètres un nombre `M < n` et la clé publique `(n,e)` et qui permet de coder `M`.

Pour coder un nombre strictement plus petit que `n`, il suffit de calculer ce nombre à la puissance `e`, modulo `n`. Pour ce faire, on dispose de la fonction `expoModulaire`.


### 2.4 Ecrire une fonction `decodageRSA` qui prend en paramètres un nombre `M < n` et la clé privée `(n,d)` et qui permet de décoder `M`.

Pour décoder un nombre strictement plus petit que `n`, il suffit de calculer ce nombre à la puissance `d`, modulo `n`. C’est la même fonction que pour coder, juste avec une clé différente en paramètre.
