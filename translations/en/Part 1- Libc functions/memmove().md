`memmove` is a byte-level memory operation function that copies `n` bytes from one memory area to another, and handles overlapping source and destination regions correctly.

#### 1. Prototype

```c
#include <string.h>

void	*memmove(void *dst, const void *src, size_t n);
				  ↑           ↑                 ↑ 
				目标地址      源地址             字节数
```

#### 2. The core feature of memmove is that it allows memory overlap

```c
dst < src   => 从前往后copy 

dst > src   => 从后往前copy

dst == src  => 什么都不用做
```

If the destination region and the source region may overlap, the copy direction is chosen based on the relative positions of `dst` and `src`:
**If the destination is ahead, copy from front to back; if the destination is behind, copy from back to front**