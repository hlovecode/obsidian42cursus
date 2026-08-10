`memmove` 是字节级内存操作函数, 把一段内存中的 `n` 个字节复制到另一段内存，并且即使源区域和目标区域发生重叠，也能够正确复制.

#### 1. Prototype

```c
void	*memmove(void *dst, const void *src, size_t n);
				  ↑           ↑                 ↑ 
				目标地址      源地址             字节数
```

#### 2. memmove 最核心的特点是允许内存重叠
