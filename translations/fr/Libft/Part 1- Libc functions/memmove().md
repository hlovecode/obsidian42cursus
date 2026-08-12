`memmove` est une fonction de manipulation de mémoire au niveau de l'octet, qui copie `n` octets d'une zone mémoire vers une autre, et ce, de manière correcte même si les zones source et destination se chevauchent.

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