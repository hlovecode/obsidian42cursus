`memcmp` 比较的是两块内存前 `n` 个字节的内容，而不是比较字符串.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

作用是