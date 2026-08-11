`memmove` est une fonction de manipulation de mémoire au niveau de l'octet, qui copie `n` octets d'une zone mémoire vers une autre, et garantit une copie correcte même si les zones source et destination se chevauchent.

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

Si les zones de destination et source risquent de se chevaucher, le sens de la copie est choisi en fonction de la position relative de `dst` et `src` :
**Destination avant la source : copie de l'avant vers l'arrière ; destination après la source : copie de l'arrière vers l'avant**