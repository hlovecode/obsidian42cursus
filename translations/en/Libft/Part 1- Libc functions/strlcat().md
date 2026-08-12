`strlcat`: **Concatenate** a string to the end of a destination string.

```
strlcat
│││
││└── cat = concatenate
││
│└── l = length-limited
│
└── str = string
```
`strlcat` can be understood as string length-limited concatenate.

#### 1. Prototype

```c
#include <string.h>

size_t strlcat(char *dst, const char *src, size_t size);
```
Its purpose is to append the `src` string to the end of the `dst` string, while using at most `size` bytes provided by `dst`.

It returns the total length of the string it tried to create. If both dst and src are normal '\0'-terminated strings, it returns `strlen(dst) + strlen(src)`. Note that this is the length of dst before concatenation.

**Note: The function parameter `size` is the total capacity of the first parameter `dst`, not the length to be appended.**

#### 2. Core Workflow of the Function

1. Find the length of the dst string.
2. Calculate how much space is left.
3. Append src.

#### 3. Returning the Full Length Even When Space is Insufficient

Example:
```c
char dst[10] = "Hello"; // 长度是5
char src[] = " World!!!"; // 长度是9
```
The string length returned by `strlcat(...)` is 14, but `dst` may actually only become "Hello Wo" with a length of 8, yet it still returns 14. This is because the function tells you: if there had been enough space, I would have produced a string of length 14. Therefore, you can check whether string truncation occurred:
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
Here `ret = 14`, `sizeof(dst) = 10`, indicating that the capacity of `dst` was insufficient and `src` was not fully appended.

#### 4. The Case Where `size = 0` in `strlcat`

For example:
```c
strlcat(dst, src, 0);
```
This means the available capacity of the target buffer is 0, so nothing can be written. However, the function still needs to compute the return value. If `dst` is a normal string:
```c
return strlen(dst) + strlen(src);
```

#### 5. `size <= current length of dst`

For example:
```c
char dst[20] = "Hello";
char src[] = "World";

strlcat(dst, src, 4);
```
Here `size = 4, strlen(dst) = 5, size < strlen(dst)`, meaning the range represented by `size` cannot even accommodate the complete `dst` string. In this case, `strlcat` should not continue accessing beyond the `size` limit to search for `'\0'`. The special return value in this case is `size + strlen(src)`, which is 4 + 5 = 9. This is a very important rule in the implementation of `strlcat`.

#### 6. Difference Between `strlcat` and `strlcpy`

| Function                        | Action                |
| ------------------------- | ----------------- |
| `strlcpy`                 | Copy string             |
| `strlcat`                 | Concatenate string             |
| `strlcpy(dst, src, size)` | `dst ← src`       |
| `strlcat(dst, src, size)` | `dst ← dst + src` |

#### 7. Implementing `ft_strlcat` Yourself

Core logic:
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
In `strlcat(dst, src, size)`, `size` is **the capacity of the entire `dst` buffer**, and the return value is **the original ``dst`` length + ``src`` length**, not the actual number of characters appended.