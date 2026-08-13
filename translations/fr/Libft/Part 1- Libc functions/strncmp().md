`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Sa fonction est de comparer octet par octet `s1` et `s2` depuis le début, jusqu'à un maximum de `n` caractères. Elle s'arrête dès qu'elle rencontre le premier caractère différent ou `\0`. Si tous les caractères comparés sont identiques, elle renvoie `0` ; sinon, elle renvoie une valeur négative ou positive selon la relation de grandeur du premier caractère différent.