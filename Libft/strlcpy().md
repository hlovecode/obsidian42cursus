`strlcpy` 是一个用于**复制 C 字符串**的函数

#### 1. Prototype

```c
size_t strlcpy(char *dst, const char *src, size_t size);
```
函数的作用是把 `src` 指向的字符串复制到 `dst`，最多写入 `size - 1` 个字符，并保证目标字符串以 `'\0'` 结尾.
返回src的完整长度，也就是strlen(src).

为什么是最多写入`size - 1`个字符 ?
因为最后一个位置是留给'\0'的，也就是dst能容纳size个bytes, 但字符最多是`size - 1`个

```
┌──────────────────────────────┐
│       dst 可以容纳 size       │
├──────────────┬───────────────┤
│ size - 1     │      1        │
│ 字符          │     '\0'      │
└──────────────┴───────────────┘
```

#### 2. 函数参数

|参数|类型|含义|
|---|---|---|
|`dst`|`char *`|目标字符串|
|`src`|`const char *`|源字符串|
|`size`|`size_t`|`dst` 能容纳的最大字节数|
注意当size == 0 时是一个很特殊的情况，这时 `size - 1`就没有意义了，因此什么都不能写入dst，包括'\0', 不会修改dst，但仍然返回strlen(src), 即返回源字符串的长度.

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

###### `strlcpy` 把 `src` 复制到容量为 `size` 的 `dst` 中，最多复制 `size - 1` 个字符，并在 `size > 0` 时保证以 `'\0'` 结尾；无论是否截断，都返回 `src` 的完整长度
对应公式：
```
size == 0
    → 不写 dst
    → return strlen(src)

size > 0
    → 最多复制 size - 1 个字符
    → dst[size相关位置] = '\0'
    → return strlen(src)
```

**一个实用的判断是否有字符串截断的方法：**
```
if (strlcpy(dst, src, sizeof(dst)) >= sizeof(dst))
{
    /* 被截断 */
}
```
`strlcpy(dst, src, sizeof(dst))` 返回`strlen(src)`, 如果:
`strlen(src) >= sizeof(dst)`, 说明`src 的完整字符串长度>= dst 可容纳的空间`

| 函数        | 操作对象 | 是否关注 `'\0'` |  是否限制目标大小 |
| --------- | ---- | ----------: | --------: |
| `strcpy`  | 字符串  |           是 |         否 |
| `strlcpy` | 字符串  |           是 |         是 |
| `memcpy`  | 任意内存 |           否 | 通过 `n` 控制 |
```
strcpy  => 复制字符串，不管目标大小

strlcpy => 复制字符串，并限制目标大小

memcpy  => 复制 n 个 byte，根本不管字符串
```

[[memcpy()]]
