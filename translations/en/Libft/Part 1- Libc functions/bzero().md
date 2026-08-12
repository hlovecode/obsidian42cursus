`bzero` is a function used to **fill a block of memory with `0`.**

#### 1. Prototype
```c
#include <strings.h>
 
void	bzero(void *s, size_t n);
```
Its purpose is to start from the memory address pointed to by `s` and set `n` consecutive bytes to `0`.
It has no return value; it simply performs a memory-modification operation.

For example:
```c
char str[10] = "abcdef";

bzero(str, 3);
```

```txt
原来的内存大概是：
地址       内容
1000       'a'
1001       'b'
1002       'c'
1003       'd'
1004       'e'
1005       'f'
1006       '\0'
...

执行bzero(str, 3)以后：
地址       内容
1000       0
1001       0
1002       0
1003       'd'
1004       'e'
1005       'f'
1006       '\0'
...
即从 `str` 开始的3个byte被清零
```

The function means: starting from address `s`, access `n` consecutive bytes, and write every single byte as `0x00`.

#### 2. Understanding the Function Parameters

1. `void *` represents the address of an object of any type.

2. `size_t n` represents how many bytes are to be cleared.
Note that this is the number of bytes, not the number of elements.

**The essential meaning of the function is `bzero(起始地址，字节数量)`.**

#### 3. Special Note: bzero works on a byte-by-byte basis
Example:
```c
int tab[5];

bzero(tab, 5);
```
It is not:
```c
tab[0] = 0
tab[1] = 0
tab[2] = 0
tab[3] = 0
tab[4] = 0
```
Instead, it only clears the first 5 bytes. Assuming `int` is 4 bytes, then:
```c
tab:

byte 0 ──┐
byte 1   │ tab[0]
byte 2   │
byte 3 ──┘

byte 4 ──┐
byte 5   │ tab[1]
byte 6   │
byte 7 ──┘
...
```
Executing `bzero(tab, 5);` will only result in:
```c
00 00 00 00 00
^^^^^^^^^^^^^^
  5 bytes
```
That is, it completely clears only `tab[0]`, and then clears the first byte of `tab[1]`, which is not the expected effect.
Therefore, the correct way to write it is:
```c
bzero(tab, sizeof(tab));
```

#### 4. Purpose of the Function

Its most typical use case is to zero out memory.

However, note that this function is not "deleting data" or freeing memory; it merely modifies the contents of the specified memory. Although the memory is zeroed out—meaning the region is set to 0—the memory remains allocated.

[[memset()]]