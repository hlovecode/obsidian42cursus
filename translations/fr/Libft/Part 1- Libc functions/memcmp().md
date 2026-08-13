`memcmp` compare le contenu des `n` premiers octets de deux blocs de mémoire, et non des chaînes de caractères.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est