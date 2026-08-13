`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Il a pour rôle de comparer `s1` et `s2` octet par octet depuis le début, sur un maximum de `n` caractères ; il s'arrête dès le premier caractère différent ou `\0`. Il renvoie `0` si tous les caractères sont identiques dans la plage de comparaison, ou une valeur négative ou positive selon la relation d'ordre du premier caractère différent.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour|
|---|---|
|Les `n` premiers caractères de `s1` sont identiques à `s2`|`0`|
|`s1` est inférieur à `s2`|`< 0`|
|`s1` est supérieur à `s2`|`> 0`|
Note : Ne dépendez pas d'une valeur exacte -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.

#### 2. Différence entre `strncmp` et `strcmp`

`strcmp` compare la chaîne entière, tandis que `strncmp` compare au maximum les n premiers caractères.

|          | strcmp     | strncmp    |
| -------- | ---------- | ---------- |
| En-tête      | <string.h> | <string.h> |
| Compare des chaînes    | oui        | oui        |
| Nombre de paramètres     | 2          | 3          |
| Limite la longueur de comparaison   | non         | oui        |
| Nombre max de caractères comparés | illimité        | n caractères      |
| Retourne 0     | Égal         | n premiers caractères égaux  |

#### 3. Application de `strncmp`

Cette fonction est idéale pour déterminer le préfixe d'une chaîne.

Par exemple : déterminer si « quit_now » commence par « quit »

```c
if (strncmp(command, "quit", 4) == 0)
{
	...
}
```

Les 3 points les plus cruciaux pour `strncmp` :

- n est le « nombre maximal de caractères à comparer », il n'est pas obligatoire de comparer n caractères.
- Il s'arrête dès le 1er caractère différent.
- Pour la valeur de retour, ne tenez compte que du signe (positif/négatif), ne dépendez pas d'un chiffre précis :

```c
if (strncmp(s1, s2, n) < 0)

if (strncmp(s1, s2, n) == 0)

if (strncmp(s1, s2, n) > 0)
```

Ne l'écrivez pas ainsi :

```c
if (strncmp(s1, s2, n) == -1)
```

Car la norme ne garantit pas qu'il retourne nécessairement -1.