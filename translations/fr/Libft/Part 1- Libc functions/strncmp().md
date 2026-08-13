`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Il a pour rôle de comparer octet par octet, à partir du début, `s1` et `s2`, sur un maximum de `n` caractères ; il peut s'arrêter dès le premier caractère différent ou `\0`. Si tous les caractères comparés sont identiques, il renvoie `0`, sinon il renvoie une valeur négative ou positive selon la relation d'ordre du premier caractère différent.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour|
|---|---|
|Les `n` premiers caractères de `s1` sont identiques à `s2`|`0`|
|`s1` est inférieur à `s2`|`< 0`|
|`s1` est supérieur à `s2`|`> 0`|
Remarque : ne dépendez pas d'un retour exact de -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.