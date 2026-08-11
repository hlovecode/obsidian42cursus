#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Son rôle est très simple : calculer le nombre de caractères dans une chaîne, à l'exclusion du `'\0` final.

#### 2. Pourquoi ne pas compter '\0' ?

En langage C, une chaîne de caractères n'est pas un type de données indépendant, c'est en réalité une suite de `char`.
Le rôle de '\0' est d'indiquer au C que la chaîne se termine ici.
Si la longueur logique de la chaîne est 5, l'espace réellement occupé dans le tableau de caractères est 6.

`strlen()` lit seulement la chaîne et ne modifie pas son contenu.
Le paramètre de la fonction doit pointer vers une chaîne C valide se terminant par '\0'.

`strlen("")` est une chaîne vide, qui correspond en réalité à `'\0'`, et la fonction retourne 0.
Remarque : une chaîne vide n'est pas dépourvue de mémoire, elle contient un `'\0'`.

`strlen(NULL)` est illégal et entraîne un comportement indéfini (*undefined behavior*), car `strlen` essaiera d'accéder à un emplacement qui ne contient aucune chaîne valide. Par conséquent, il ne faut pas écrire :
```c
char *str = NULL;
strlen(str);
```
N'utilisez pas non plus `strlen` pour vérifier si `str` est `NULL`, n'écrivez pas :
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

Il s'agit d'un type d'entier non signé `unsigned int` ou `unsigned long`, déclaré et défini par `<stddef.h>`. C'est le type le plus sûr pour tout objet de données entier utilisé comme indice de tableau, sans avoir à craindre qu'un petit tableau ne devienne très grand au fil des modifications du programme.

Lors de l'utilisation de `size_t`, l'arithmétique des indices ne subira jamais de dépassement (*overflow*). Partout dans le programme où l'on effectue des opérations arithmétiques sur des indices de tableaux ou des adresses, il convient d'utiliser le type `size_t`. Son seul inconvénient est qu'il ne peut pas accepter de valeurs négatives.

`size_t` est un type d'entier non signé défini par le standard C, spécialement conçu pour représenter :
- La taille d'un objet
- La taille d'un tableau
- La taille de la mémoire
- Le nombre d'octets