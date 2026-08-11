`strlcpy` is a function used for **copying C strings**

#### 1. Prototype

```c
#include <string.h>

size_t strlcpy(char *dst, const char *src, size_t size);
```
The function copies the string pointed to by `src` to `dst`, writing at most `size - 1` characters, and guarantees that the destination string is terminated with `'\0'`.
It returns the full length of src, which is strlen(src).

Why is it at most `size - 1` characters written?
Because the last position is reserved for '\0', meaning dst can hold size bytes, but the maximum number of characters is `size - 1`.

```
┌──────────────────────────────┐
│       dst 可以容纳 size       │
├──────────────┬───────────────┤
│ size - 1     │      1        │
│ 字符          │     '\0'      │
└──────────────┴───────────────┘
```

#### 2. Function Parameters

|Parameter|Type|Meaning|
|---|---|---|
|`dst`|`char *`|Destination string|
|`src`|`const char *`|Source string|
|`size`|`size_t`|Maximum number of bytes that `dst` can hold|

Note that when size == 0, it is a very special case. In this scenario, `size - 1` has no meaning, so nothing can be written to dst, including '\0'. dst will not be modified, but it still returns strlen(src), which is the length of the source string.

```
                 strlcpy(dst, src, size)
                              │
                 ┌────────────┴────────────┐
                 │                         │
              size == 0                size > 0
                 │                         │
              不写任何东西            最多写 size-1 字符
                 │                         │
                 │                    最后写 '\0'
                 │
                 └────────────┬────────────┘
                              ↓
                       返回 strlen(src)
```

###### `strlcpy` copies `src` to `size` with a capacity of `dst`, copying at most `size - 1` characters, and guarantees termination with `size > 0` upon `'\0'`; regardless of whether truncation occurs, it returns the full length of `src`
Corresponding formula:
```
size == 0
    → 不写 dst
    → return strlen(src)

size > 0
    → 最多复制 size - 1 个字符
    → dst[size相关位置] = '\0'
    → return strlen(src)
```

**A practical method to determine whether string truncation has occurred:**
```
if (strlcpy(dst, src, sizeof(dst)) >= sizeof(dst))
{
    /* 被截断 */
}
```
`strlen(src) >= sizeof(dst)` returns `strlen(src)`, if:
`strlen(src) >= sizeof(dst)`, it indicates `src 的完整字符串长度>= dst 可容纳的空间`

| Function        | Target Object | Cares about `'\0'`? | Limits Destination Size? |
| --------- | ---- | ----------: | --------: |
| `strcpy`  | String  |           Yes |         No |
| `strlcpy` | String  |           Yes |         Yes |
| `memcpy`  | Arbitrary Memory |           No | Controlled via `n` |
```
strcpy  => 复制字符串，不管目标大小

strlcpy => 复制字符串，并限制目标大小

memcpy  => 复制 n 个 byte，根本不管字符串
```

[[memcpy()]]