
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

#### 4. `strrchr` 的常用场景是 ”获取文件扩展名“

例1：`strrchr` 在处理文件路径，文件名时非常常见

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

结果指针 p 指向 document.txt 的 `.txt`，所以：

```c
printf("%s\n", p); // .txt
```

例2：再看一个路径例子, 我们想找到最后一个 `/`, 可以：

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p 指向字符串 ”/Users/lee/project/main.c" 的最后一个 `/`, 那么：

```c
printf("%s\n", p + 1);
```

得到 `main.c`