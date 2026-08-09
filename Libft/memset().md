`memset` 是 C 语言里非常重要的一个**内存操作函数**，它直接修改一块内存中的每一个字节.

#### 1. Prototype

```c
#include <string.h>

void	*memset(void *s, int c, size_t n);
```
它的作用可以简单理解成从 s 开始，把连续的 n 个字节全部设置成 c 的低8位. 
它的3个参数：
```txt
             memset
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      s         c        n
      │         │        │
      ↓         ↓        ↓
   起始地址    要设置的   设置多少
               字节值     个字节
```
返回被修改的内存区域的起始地址 s，类型是`void *`，一个通用的内存地址. 

`memset` 从某个地址开始，修改 n 个字节，当n == 0时，表示修改 0 个字节，不会修改任何东西，可以理解为什么都不做. 
注意 n 是 byte 数量，不是元素数量. 

`memset(s, c, n)`：从地址 `s` 开始，把连续的 `n` 个字节都写成 `c` 的低 8 位，并返回 `s`

#### 2. 理解函数参数

1. 第1个参数 `void *s`
表示要操作的内存区域的起始地址，`void *` 是因为 memset 不关系你传进去的到底是什么类型，它操作的是字节(byte), 而不是char, int, double 等C类型.
例如：
```c
char str[10];
int tab[10];
double values[10];
```
都可以：
```c
memset(str, ...);
memset(tab, ...);
memset(values, ...);
```

2. 第2个参数 `int c`
把 n 个字节设置成 c 转换后的 unsigned char 值. 
例如：
```c
char str[5];

memset(str, 'A', 5);
```
'A' 的 ASCII 值：'A' = 65 = 0x41
所以 65 转成16进制0x41，每个字节都会变成41 41 41 41 41, 也就是A A A A A

3. 第3个参数 `size_t n`
表示要修改多少个字节
例如：
```c
char str[10];

memset(str, 'A', 3);
```
表示：
```txt
第 0 个字节 → A
第 1 个字节 → A
第 2 个字节 → A
```
一共是3 bytes

PS: 通常一个 int 是 4 bytes 

#### 3. memset 最常见的用途

1. 把数组清零
```c
int tab[100];

memset(tab, 0, sizeof(tab));
```

2. 初始化结构体
```c
struct person
{
	char	name[50];
	int		age;
};

memset(&p, 0, sizeof(p)); // 把整个结构体占用的字节设置为0
```

3. 清空字符数组
```c
char buffer[1024];

memset(buffer, 0, sizeof(buffer));
```
结果：
```c
buffer[0] = '\0'
buffer[1] = '\0'
buffer[2] = '\0'
...
```

4. 设置一块内存为特定字节
```c
char buffer[10];

memset(buffer, 'X', 10);
```
得到：
```txt
X X X X X X X X X X
```

```txt
① s 是起始地址
        ↓
② 转成 unsigned char *
        ↓
③ i 从 0 开始
        ↓
④ 每次修改 1 byte
        ↓
⑤ 修改 n 次
        ↓
⑥ 返回原来的 s
```
