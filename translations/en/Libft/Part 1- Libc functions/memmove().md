`memmove` is a byte-level memory operation function that copies `n` bytes from one memory region to another, ensuring correct copying even if the source and destination regions overlap.

#### 1. Prototype

```c
#include <string.h>

void	*memmove(void *dst, const void *src, size_t n);
				  ↑           ↑                 ↑ 
				目标地址      源地址             字节数
```

#### 2. The core feature of memmove is that it allows overlapping memory

```c
dst < src   => 从前往后copy 

dst > src   => 从后往前copy

dst == src  => 什么都不用做
```

If the destination region and the source region may overlap, the copying direction is chosen based on the relative positions of `dst` and `src`:
**If the destination is ahead, copy from front to back; if the destination is behind, copy from back to front.**