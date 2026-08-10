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
注意该函数不是专门复制字符串的.

#### 2. 函数参数

从 `src` 开始读取 `n` 个字节，然后写入 `dest`.

|参数|含义|
|---|---|
|`dest`|destination，目标地址|
|`src`|source，源地址|
|`n`|要复制多少个 byte|
- dest : 目标内存区域的起始地址
- src: 