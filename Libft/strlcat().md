`strlcat`：把一个字符串 **追加（concatenate）** 到目标字符串后面

#### 1. Prototype

```c
#include <string.h>

size_t strlcat(char *dst, const char *src, size_t size);
```
作用是把 `src` 字符串追加到 `dst` 字符串的末尾，同时最多只使用 `dst` 所提供的 `size` 个字节.