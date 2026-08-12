
strrchr 在一个字符串中查找某个字符最后一次出现的位置.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

作用是从左往右搜索，但返回字符最后一次出现的位置.
具体实现可以从前往后扫描字符串，也可以从后往前扫描字符串.

#### 2. `strrchr` 和 `strchr` 的区别

例如：“hello world" 里的字母 o 出现了2次

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr`：从左往右找字符，返回字符第一次出现的位置
 - `strrchr`：从左往右搜索，但返回最后一次出现的位置

#### 3. `strrchr` 的返回值

返回值类型是 `char *`, 返回找到的字符的地址，找不到字符则返回 NULL.

`strrchr` 的一个重要特点是它会搜索 '\0', 也就是它会返回字符串结束符 '\0' 的地址.



