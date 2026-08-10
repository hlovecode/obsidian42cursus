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

**注意函数参数 size 是第1个参数 dst 的总容量，而不是追加长度**

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

#### 4. strlcat 的 size = 0 的情况

例如：
```c
strlcat(dst, src, 0);
```
意味着目标缓冲区可用容量为0，所以不能写任何东西. 但是函数仍然需要计算返回值，如果 dst 是正常字符串：
```c
return strlen(dst) + strlen(src);
```

#### 5. size <= dst 当前长度

例如：
```c
char dst[20] = "Hello";
char src[] = "World";

strlcat(dst, src, 4);
```
这里`size = 4, strlen(dst) = 5, size < strlen(dst)`, 意味着 size 所表示的范围甚至无法容纳完整的 dst 字符串，这种情况下，strlcat 不应该继续访问超过 size 的范围寻找 '\0', 返回的特殊情况是 `size + strlen(src)`, 即 4 + 5 = 9. 这是strlcat 实现里非常重要的一条规则.

#### 6. strlcat 和 strlcpy 的区别

| 函数                        | 作用                |
| ------------------------- | ----------------- |
| `strlcpy`                 | 复制字符串             |
| `strlcat`                 | 追加字符串             |
| `strlcpy(dst, src, size)` | `dst ← src`       |
| `strlcat(dst, src, size)` | `dst ← dst + src` |

#### 7. 自己实现ft_strlcat

核心思路：
```txt
1. 找 dst 的长度
2. 找 src 的长度
3. 判断 size 是否足够，如果 size <= dst_len：返回 size + src_len
   否则：计算最多可以追加多少字符
   最多追加的字符数 = size - dst_len - 1
4. 如果足够，把 src 全部追加
5. 如果不够，只追加能够容纳的部分
6. 最后添加 '\0'
7. 返回“原 dst 长度 + src 长度”
   
   
                size
                 │
                 ▼
        ┌─────────────────┐
        │   dst 总容量     │
        └─────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
    dst_len          剩余空间
                         │
                         ▼
                  size-dst_len-1
                         │
                         ▼
                    追加 src
```
`strlcat(dst, src, size)` 中的 `size` 是 **dst 整个缓冲区的容量**，而返回值是 **原 `dst` 长度 + `src` 长度**，不是实际追加了多少字符