`strlcat`：把一个字符串 **追加（concatenate）** 到目标字符串后面

```
strlcat
│││
││└── cat = concatenate
││
│└── l = length-limited
│
└── str = string
```
strlcat 可以理解为 string length-limited concatenate (有长度限制的字符串拼接)

#### 1. Prototype

```c
#include <string.h>

size_t strlcat(char *dst, const char *src, size_t size);
```
作用是把 `src` 字符串追加到 `dst` 字符串的末尾，同时最多只使用 `dst` 所提供的 `size` 个字节.
返回试图创建的完整字符串长度，如果dst 和 src 都是正常的，以 '\0' 结尾的字符串，那么返回 `strlen(dst) + strlen(src)`, 注意是追加之前 dst 的长度.

#### 2. 函数的核心工作过程

1. 找到 dst 的字符串长度
2. 计算还能放多少空间
3. 追加src

#### 3. 空间不足时还是返回完整长度

举例说明：
```c
char dst[10] = "Hello"; // 长度是5
char src[] = " World!!!"; // 长度是9
```
strlcat(...) 返回的字符串长度是14，但dst 实际可能只能变成 ”Hello Wo", 长度是8，但还是返回14. 因为该函数告诉你，如果空间足够，我本来想得到一个长度为14的字符串，因此可以判断是否发生字符串截断：
```c
char dst[10] = "Hello";
char src[] = " World!!!";

size_t ret;

ret = strlcat(dst, src, sizeof(dst));

if (ret >= sizeof(dst))
{
	printf("字符串被截断了\n");
}
```
这里 ret = 14, sizeof(dst) = 10, 说明 dst 的容量不足， src 没有完整追加

