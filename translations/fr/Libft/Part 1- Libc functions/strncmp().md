`strncmp` compare au plus les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Sa fonction est de comparer octet par octet, du début, `s1` et `s2`, en comparant au maximum `n` caractères ; elle peut s'arrêter dès le premier caractère différent ou à `\0`. Si tous les caractères de la plage comparée sont identiques, elle renvoie `0`, sinon elle renvoie une valeur négative ou positive selon la relation de grandeur du premier caractère différent.

fanyifanyi