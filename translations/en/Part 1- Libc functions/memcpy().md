`memcpy`: Copy the contents of one memory block to another.

#### 1. Prototype

```c
#include <string.h>

void	*memcpy(void *dest, const void *src, size_t n);
```
Its function is to copy `n` bytes from the memory area pointed to by `src` to the memory area pointed to by `dest`.
It can be understood as:
```txt
src  ──────────────► 读取
                      │
                      │ n 个 byte
                      ▼
dest ──────────────► 写入
```
Returns the starting address of the destination memory area. 

Note that this function is not specifically for copying strings; it does not care what the data is. Essentially, it is a byte-by-byte copy of raw memory, which is also why it can copy structures—it copies the entire memory occupied by the structure. 

#### 2. Function Parameters

Read `n` bytes starting from `src`, then write to `dest`.

|Parameter|Meaning|
|---|---|
|`dest`|destination, destination address|
|`src`|source, source address|
|`n`|Number of bytes to copy|
- dest : The starting address of the destination memory area
- src: The starting address of the source memory area. `const void *src` indicates that the data pointed to by `src` cannot be modified within this function.

#### 3. Precautions

- memcpy does not automatically append `'\0'`
- memcpy cannot handle overlapping memory, meaning it cannot handle situations where the source and destination areas might overlap; it is `undefined behavoir`. To handle overlapping memory, use `memmove()`.
- When $n = 0$, i.e., `memcpy(dest, src, 0)`, 0 bytes are copied, so no actual data is copied, but the function still returns `dest`.
- `dest` and `src` must have sufficient space; this is a very important security issue. 

[[strlcpy()]]