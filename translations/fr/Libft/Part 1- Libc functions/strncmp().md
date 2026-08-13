`strncmp` compare au plus les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Sa fonction est de comparer octet par octet `s1` et `s2` depuis le début, en comparant au plus `n` caractères ; elle s'arrête dès le premier caractère différent ou `\0`. Si tous les caractères dans la plage comparée sont identiques, elle renvoie `0`, sinon elle renvoie une valeur négative ou positive selon la relation de grandeur du premier caractère différent.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour|
|---|---|
|Les `n` premiers caractères de `s1` sont identiques à `s2`|`0`|
|`s1` est inférieur à `s2`|`< 0`|
|`s1` est supérieur à `s2`|`> 0`|
Remarque : ne vous fiez pas à des valeurs spécifiques telles que -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.

#### 2. Différence entre `strncmp` et `strcmp`

`strcmp` compare la chaîne entière, tandis que `strncmp` compare au plus les n premiers caractères.