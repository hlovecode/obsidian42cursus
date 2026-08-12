`memcpy`：把一块内存中的内容，复制到另一块内存中.

#### 1. Prototype

```c
#include <string.h>

void	*memcpy(void *dest, const void *src, size_t n);
```
它的作用是从 `src` 指向的内存区域开始，复制 `n` 个字节到 `dest` 指向的内存区域.
可以理解成：
```txt
src  ──────────────► 读取
                      │
                      │ n 个 byte
                      ▼
dest ──────────────► 写入
```
返回目标内存区域的起始地址. 

注意该函数不是专门复制字符串的，它不关心数据是什么，本质上是原始内存的byte-by-byte copy, 这也是为什么它可以复制结构体, 复制的是整个结构体占用的内存. 

#### 2. 函数参数

从 `src` 开始读取 `n` 个字节，然后写入 `dest`.

|参数|含义|
|---|---|
|`dest`|destination，目标地址|
|`src`|source，源地址|
|`n`|要复制多少个 byte|
- dest : 目标内存区域的起始地址
- src: 源内存区域的起始地址, const void \*src 表示 src 指向的数据在这个函数里面不能被修改

#### 3. 注意事项

- memcpy 不会自动添加 '\0'
- memcpy 不能处理处理重叠内存, 也就是不能处理源区域和目标区域可能重叠的情况,是`undefined behavoir`, 处理重叠内存要使用`memmove()`
- 当n = 0，即memcpy(dest, src, 0) 复制0个byte，所以没有实际数据复制，但函数仍然返回dest
- dest 和 src 必须有足够空间，这是非常重要的安全问题. 

[[strlcpy()]]
