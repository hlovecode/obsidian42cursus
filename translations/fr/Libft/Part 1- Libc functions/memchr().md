`memchr` Recherche un octet dans les `n` premiers octets d'un bloc de mémoire, sans se soucier du tout de `'\0'`.
`memchr` Recherche l'octet btye et non un caractère. C'est simplement que lorsqu'on recherche une chaîne ASCII normale, un caractère occupe généralement exactement un octet, ce qui donne l'impression de rechercher un caractère.
Cette fonction lit uniquement la mémoire et ne la modifie pas.

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Son rôle est de commencer à partir de la zone mémoire `s`, de vérifier les `n` premiers octets et de chercher le premier octet dont la valeur est égale à `(unsigned char)c`. 

Valeur de retour :

- Si l'octet est trouvé, renvoie un pointeur vers celui-ci.
- S'il n'est pas trouvé, renvoie NULL.

#### 2. `memchir` peut traiter des données sans '\0'

L'une des plus grandes différences entre `memchr` et les autres fonctions de chaînes est qu'elle peut traiter des données sans '\0'. Elle n'a pas besoin de '\0' pour déterminer la fin, elle dépend uniquement de n. 

`memchr` vérifie essentiellement octet par octet et peut traiter n'importe quelle mémoire.

#### 3.  `memchir`  vs  `strchr` 

|Caractéristique|`strchr`|`memchr`|
|---|---|---|
|Appartenance|`<string.h>`|`<string.h>`|
|Objet de la recherche|Chaîne C|Zone mémoire|
|Nécessite `'\0'`|Oui|Non|
|S'arrête-t-il dès `'\0'`|Oui|Non|
|Portée de la recherche|Jusqu'à `'\0'`|Les `n` premiers octets|
|Paramètre `n`|Non|Oui|
|Peut rechercher des données binaires|Inadapté|Très adapté|
|Valeur de retour|`char *`|`void *`|
|Introuvable|`NULL`|`NULL`|

- `strchr` : Recherche un caractère dans une chaîne
- `memchr` : Recherche un octet dans la mémoire

#### 4. Idée d'implémentation de `memchr`

1. Convertir s en unsigned char *
2. Commencer la vérification à partir de i = 0 tant que i < n
3. Vérifier si s\[i] est égal à (unsigned char)c :
	- S'ils sont égaux, renvoyer `&s[i]`
	- S'ils ne sont pas égaux, i++
	- Fin de la boucle : si c'est toujours pas égal, renvoyer NULL


```c
<string.h>

void *memchr(const void *s, int c, size_t n);
``` commence à partir de `s`, considère la mémoire comme une séquence d'octets, vérifie strictement les `n` premiers octets à la recherche du premier octet égal à `(unsigned char)c` ; s'il est trouvé, renvoie son adresse, sinon renvoie `NULL`.