`memcmp` compare les contenus des deux premiers `n` octets de mémoire, et non pas des chaînes de caractères.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux zones de mémoire commençant respectivement à `s1` et `s2`.

Valeur de retour :

| Résultat de la comparaison | Valeur de retour de `memcmp` |
|---|---|
| Les deux blocs de mémoire sont strictement identiques | `0` |
| Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2` | Inférieur à `0` |
| Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2` | Supérieur à `0` |

La norme C garantit seulement le signe de la valeur de retour (positif, négatif ou zéro), mais pas la valeur exacte. Cela signifie qu'il faut effectuer l'une des vérifications ci-dessous, et non pas `memcmp(s1, s2, n) == -1`, car la norme C ne stipule pas qu'elle doit nécessairement retourner -1 :

```c
if (memcmp(s1, s2, n) > 0)

if (memcmp(s1, s2, n) == 0)

if (memcmp(s1, s2, n) < 0)
```