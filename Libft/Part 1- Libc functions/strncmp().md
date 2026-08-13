
`strncmp` 最多只比较前 `n` 个字符.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

作用是从头开始逐字节比较 `s1` 和 `s2`，最多比较 `n` 个字符；遇到第一个不同字符或 `\0` 就可以停止，如果比较范围内全部相同则返回 `0`，否则根据第一个不同字符的大小关系返回负值或正值.

fanyifanyi 
