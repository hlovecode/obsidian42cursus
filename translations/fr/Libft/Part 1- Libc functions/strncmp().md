`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Sa fonction est de comparer octet par octet `s1` et `s2` depuis le début, en comparant au maximum `n` caractères ; elle peut s'arrêter dès le premier caractère différent ou `\0`. Si toutes les valeurs dans la plage de comparaison sont identiques, elle renvoie `0`, sinon elle renvoie une valeur négative ou positive selon la relation de grandeur du premier caractère différent.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour|
|---|---|
|Les `n` premiers caractères de `s1` sont identiques à `s2`|`0`|
|`s1` est inférieur à `s2`|`< 0`|
|`s1` est supérieur à `s2`|`> 0`|
Remarque : ne vous fiez pas à des valeurs de retour spécifiques telles que -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.

#### 2. Différence entre `strncmp` et `strcmp`

`strcmp` compare la chaîne entière, tandis que `strncmp` compare au maximum les n premiers caractères.

|          | strcmp     | strncmp    |
| -------- | ---------- | ---------- |
| En-tête      | <string.h> | <string.h> |
| Compare des chaînes    | oui        | oui        |
| Nombre de paramètres     | 2          | 3          |
| Limite la longueur de comparaison   | non         | oui        |
| Nombre max. de caractères comparés | Illimité        | n caractères      |
| Renvoie 0     | Égal         | n premiers caractères égaux  |

#### 3. Application de `strncmp`

Cette fonction est idéale pour déterminer le préfixe d'une chaîne de caractères.

Par exemple : déterminer si "quit_now" commence par quit

```c
if (strncmp(command, "quit", 4) == 0)
{
	...
}
```