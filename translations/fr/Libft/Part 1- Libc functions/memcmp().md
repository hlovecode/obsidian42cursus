`memcmp` compare le contenu des `n` premiers octets de deux blocs mémoires, et non des chaînes de caractères.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux régions mémoires commençant respectivement à `s1` et `s2`.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour de `memcmp`|
|---|---|
|Les deux blocs mémoires sont totalement identiques|`0`|
|Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2`|Inférieur à `0`|
|Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2`|Supérieur à `0`|

La norme C garantit uniquement le signe de la valeur de retour (positif, négatif ou nul), et non sa valeur exacte. C'est-à-dire qu'il faut effectuer l'un des tests suivants, et non :

```c
if (memcmp(s1, s2, n) > 0)

if (memcmp(s1, s2, n) == 0)

if (memcmp(s1, s2, n) < 0)
```