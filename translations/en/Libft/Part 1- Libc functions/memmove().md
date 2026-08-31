`memmove` is a byte-level memory operation function that copies `n` bytes from one memory area to another, and can correctly copy even if the source and destination areas overlap.

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

If the destination area and source area may overlap, according to the relative positions of `dst` and `src`, select the copy direction:
**Destination before source, from front to back; destination after source, from back to front**

---

## 中文原文

`memmove` 是字节级内存操作函数, 把一段内存中的 `n` 个字节复制到另一段内存，并且即使源区域和目标区域发生重叠，也能够正确复制.

#### 1. Prototype

```c
#include <string.h>

void	*memmove(void *dst, const void *src, size_t n);
				  ↑           ↑                 ↑ 
				目标地址      源地址             字节数
```

#### 2. memmove 最核心的特点是允许内存重叠

```c
dst < src   => 从前往后copy 

dst > src   => 从后往前copy

dst == src  => 什么都不用做
```

如果目标区域和源区域可能重叠，就根据 `dst` 和 `src` 的相对位置选择复制方向：
**目标在前，从前往后；目标在后，从后往前**
