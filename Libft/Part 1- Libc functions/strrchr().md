
strrchr 在一个字符串中查找某个字符最后一次出现的位置.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

作用是从左往右搜索，但返回字符最后一次出现的位置.
具体实现可以从前往后扫描字符串，也可以从后往前扫描字符串.

#### 2. `strrchr` 和 `strchr`


