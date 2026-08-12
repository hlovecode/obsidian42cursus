
`strrchr` 遍历一个 C 字符串，寻找字符 `c` 最后一次出现的位置，并返回指向该位置的指针；如果没有找到，则返回 `NULL`.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

作用是从左往右搜索，但返回字符最后一次出现的位置.

具体实现可以从前往后扫描字符串，也可以从后往前扫描字符串：

1. 一个典型的从前往后找字符的思路是：从字符串开头开始遍历，每次发现目标字符，就更新最后一次出现的位置. 不是找到一次就 return, 而是每找到一次，就覆盖上一次的位置. 
	这种方法的优点：
		- 不需要先计算字符串长度
		- 可以顺便处理 '\0'
		- 思路非常稳定

2. 还有一种直观的方法是从后往前找，从最后一个字符开始扫描往前寻找
	优点是：
		- 逻辑非常符合 `strrchr` 的名字
		- 找到第一次就可以直接返回，因为它就是最后一次出现
	缺点是：
		- 通常需要先计算长度
		- 如果自己调用 `ft_strlen`，会多一次遍历

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

`strrchr` 的一个重要特点是它会搜索 '\0', 也就是它会返回字符串结束符 '\0' 的地址，
因此扫描字符串的时候一定要记得检查 '\0'.

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

得到 `/main.c`, p + 1 指向 `main.c` , 所以经常可以看到下面的写法：

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```