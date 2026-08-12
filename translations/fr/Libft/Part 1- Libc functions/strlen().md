#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Son rôle est très simple : calculer le nombre de caractères dans une chaîne, mais sans inclure le `'\0` de fin. 

#### 2. Pourquoi ne pas compter '\0' ?

En langage C, les chaînes de caractères ne constituent pas un type de données indépendant ; elles sont en réalité une suite de `char`. 
Le rôle de '\0' est d'indiquer au C que la chaîne se termine ici. 
Si la longueur logique de la chaîne est de 5, l'espace réellement occupé dans le tableau de caractères est de 6.

strlen() se contente de lire la chaîne et ne modifie pas son contenu.
Le paramètre de la fonction doit pointer vers une chaîne C valide et se terminant par '\0'.

strlen("") correspond à une chaîne vide, qui est en réalité '\0', et la fonction renvoie 0.
Remarque : une chaîne vide n'est pas dépourvue de mémoire, elle contient un '\0'.

strlen(NULL) est illégal et constitue un comportement indéfini (*undefined behavior*), car strlen essaiera d'accéder à une adresse qui ne contient aucune chaîne valide. Par conséquent, il ne faut pas écrire :

```c
char *str = NULL;
strlen(str);
```
N'utilisez pas non plus strlen pour déterminer si str est NULL, n'écrivez pas :
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

Il s'agit d'un type d'entier non signé `unsigned int` ou `unsigned long`, déclaré et défini par `<stddef.h>`. C'est le type le plus sûr pour tout objet de données entier utilisé comme indice de tableau, car il évite de craindre qu'un petit tableau ne devienne très grand au fil des modifications du programme.

Lors de l'utilisation de `size_t`, l'arithmétique des indices ne subira jamais de dépassement (*overflow*). Partout dans le programme où l'on effectue des opérations arithmétiques sur des indices de tableaux ou des adresses, il convient d'utiliser le type `size_t` ; son seul inconvénient est qu'il ne peut pas accepter de valeurs négatives. 

`size_t` est un type d'entier non signé défini par la norme C, spécifiquement dédié à la représentation de :
- La taille d'un objet
- La taille d'un tableau
- La taille de la mémoire
- Le nombre d'octets


## GitHub Actions 测试

Cette traduction est un test automatique via GitHub Actions.