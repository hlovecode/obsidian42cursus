`memchr` Recherche un octet dans les `n` premiers octets d'un bloc de mémoire, sans se soucier du tout de `'\0'`.
`memchr` Recherche l'octet byte et non un caractère. C'est simplement que lors de la recherche d'une chaîne ASCII classique, un caractère occupe généralement exactement un octet, ce qui donne l'impression de rechercher un caractère.
Cette fonction lit uniquement la mémoire et ne la modifie pas.

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Son rôle est de commencer à partir de la zone mémoire `s`, d'examiner les `n` premiers octets à la recherche du premier octet dont la valeur est égale à `(unsigned char)c`. 

Valeur de retour :

- Si trouvé, renvoie un pointeur vers cet octet
- Si non trouvé, renvoie NULL

#### 2. `memchr` peut traiter des données sans '\0'

L'une des plus grandes différences entre `memchr` et les autres fonctions de chaînes de caractères est qu'elle peut traiter des données sans '\0'. Elle n'a pas besoin de '\0' pour déterminer la fin, elle dépend uniquement de n. 

`memchr` effectue essentiellement une vérification octet par octet et peut traiter n'importe quelle mémoire.

#### 3.  `memchr`  vs  `strchr` 

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
2. Commencer à vérifier à partir de i = 0 tant que i < n
3. Vérifier si s\[i] est égal à (unsigned char)c :
	- S'ils sont égaux, renvoyer `&s[i]`
	- S'ils ne sont pas égaux, i++
	- Fin de la boucle, si toujours pas égaux, renvoyer NULL


___PROTECTED_34___ `memchr(s, c, n)` commence à `s`, considère la mémoire comme une suite d'octets, examine strictement les `n` premiers octets à la recherche du premier octet égal à `(unsigned char)c` ; s'il le trouve, il renvoie son adresse, sinon il renvoie `NULL`.