`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Sa fonction est de comparer octet par octet, depuis le début, `s1` et `s2`, sur un maximum de `n` caractères. Elle s'arrête dès qu'elle rencontre le premier caractère différent ou `\0`. Si tous les caractères de la plage comparée sont identiques, elle renvoie `0` ; sinon, elle renvoie une valeur négative ou positive selon la relation d'ordre du premier caractère différent.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour|
|---|---|
|Les `n` premiers caractères de `s1` sont identiques à `s2`|`0`|
|`s1` est inférieur à `s2`|`< 0`|
|`s1` est supérieur à `s2`|`> 0`|
Attention : ne dépendez pas d'une valeur exacte de -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.

#### 2. Différence entre `strncmp` et `strcmp`

`strcmp` compare la chaîne entière, tandis que `strncmp` compare au maximum les n premiers caractères.

|          | strcmp     | strncmp    |
| -------- | ---------- | ---------- |
| En-tête      | <string.h> | <string.h> |
| Compare des chaînes | oui        | oui        |
| Nombre de paramètres     | 2          | 3          |
| Limite la longueur de comparaison   | non         | yes        |
| Nombre max de caractères comparés | Illimité        | n caractères      |
| Renvoie 0     | Égales         | Les n premiers caractères sont égaux  |

#### 3. Application de `strncmp`

Cette fonction est idéale pour déterminer le préfixe d'une chaîne de caractères.

Par exemple : déterminer si "quit_now" commence par quit

```c
if (strncmp(command, "quit", 4) == 0)
{
	...
}
```

Les 3 points les plus cruciaux de `strncmp` :

- n est le "nombre maximal de caractères à comparer", et non le nombre exact de caractères à comparer.
- Elle s'arrête dès le 1er caractère différent.
- Pour la valeur de retour, ne tenez compte que du signe (positif/négatif) et ne dépendez pas d'un chiffre spécifique :

```c
if (strncmp(s1, s2, n) < 0)

if (strncmp(s1, s2, n) == 0)

if (strncmp(s1, s2, n) > 0)
```

Ne l'écrivez pas ainsi :

```c
if (strncmp(s1, s2, n) == -1)
```

Car la norme ne garantit pas qu'elle renverra systématiquement -1. 

L'essence de `strncmp` est de :

- Dans une fenêtre de taille maximale `n`, rechercher le premier caractère différent entre `s1` et `s2`
- Dès qu'il est trouvé, on le compare ; si rien n'est trouvé, on renvoie 0