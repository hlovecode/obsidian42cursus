`memcmp` compares the contents of the first `n` bytes of two memory blocks, rather than comparing strings.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Its function is