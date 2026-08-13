`memchr` 在一块内存的前 `n` 个字节中查找某个字节，它根本不关心 `'\0.
`memchr` 搜索的是字节 btye, 而不是字符，只是当搜索的是普通 ASCII 字符串时，一个字符通常刚好占一个 byte, 所以看起来好像是在搜索字符.
该函数只读取内存，不修改内存. 

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

它的作用是从从内存区域 `s` 开始，检查前 `n` 个字节，寻找第一个值等于 `(unsigned char)c` 的字节. 

返回值：

- 如果找到，返回指向这个字节的指针
- 如果没有找到，则返回 NULL

#### 2. 