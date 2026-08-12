#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Son rôle est très simple : calculer le nombre de caractères dans une chaîne, mais sans inclure le `'\0` de fin. 

#### 2. Pourquoi ne pas compter '\0' ?

En langage C, les chaînes de caractères ne constituent pas un type de données indépendant, ce sont en réalité des suites de `char`. 
Le rôle de '\0' est d'indiquer au C que la chaîne se termine ici. 
Si la longueur logique de la chaîne est de 5, l'espace réellement occupé dans le tableau de caractères est de 6.

`strlen()` lit uniquement la chaîne de caractères et ne modifie pas son contenu.
Le paramètre de la fonction doit pointer vers une chaîne C valide se terminant par '\0'.

`strlen("")` est une chaîne vide, qui est en réalité constituée de '\0', et la fonction renvoie 0.
Remarque : une chaîne vide n'est pas dépourvue de mémoire, elle contient un '\0'.

`strlen(NULL)` est illégal et provoque un comportement indéfini (*undefined behavior*), car `strlen` essaie d'accéder à une chaîne qui n'a aucune existence valide. Par conséquent, il ne faut pas écrire :
```c
char *str = NULL;
strlen(str);
```
N'utilisez pas non plus `strlen` pour déterminer si `str` est `NULL`, n'écrivez pas :
```c
if (strlen(str) == 0) 来判断 str == NULL
```
La bonne façon de faire est :
```c
if (str == NULL)
{
	/* NULL */
	...
}
else if (strlen(str) == 0)
{
	/* empty string */
	...
}
```

#### 3. Le type size_t

Il s'agit d'un type d'entier non signé `unsigned int` ou `unsigned long`, déclaré et défini par `<stddef.h>`. C'est le type le plus sûr pour représenter l'indice d'un tableau ou tout objet de données entier, sans avoir à craindre qu'un petit tableau ne devienne très grand au fil des modifications du programme.

Lors de l'utilisation de `size_t`, l'arithmétique des indices ne subit jamais de dépassement (*overflow*). Partout dans le programme où l'on effectue des opérations arithmétiques sur des indices de tableaux ou des adresses, on devrait utiliser le type `size_t` ; son seul inconvénient est de ne pas pouvoir accepter de valeurs négatives. 

`size_t` est un type entier non signé défini par le standard C, spécialement conçu pour représenter :
- La taille des objets
- La taille des tableaux
- La taille de la mémoire
- Le nombre d'octets


## Test GitHub Actions

Ceci est un test de traduction automatique via GitHub Actions.