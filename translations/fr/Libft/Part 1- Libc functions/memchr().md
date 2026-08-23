`memchr` 在一块内存的前 `n` 个字节中查找某个字节，它根本不关心 `'\0'`.
`memchr` 搜索的是字节 byte，而不是字符，只是当搜索的是普通 ASCII 字符串时，一个字符通常刚好占一个 byte，所以看起来好像是在搜索字符.
该函数只读取内存，不修改内存. 

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

它的作用是从内存区域 `s` 开始，检查前 `n` 个字节，寻找第一个值等于 `(unsigned char)c` 的字节. 

返回值：

- 如果找到，返回指向这个字节的指针
- 如果没有找到，则返回 NULL

#### 2. `memchr` 可以处理没有 '\0' 的数据

`memchr` 和其他字符串函数最大的区别之一就是它可以处理没有 '\0' 的数据，它不需 '\0' 来确定结束位置，它只依赖 n. 

`memchr` 本质上是逐字节检查，它可以处理任意内存.

#### 3.  `memchr`  vs  `strchr` 

| Caractéristique | `strchr` | `memchr` |
|---|---|---|
| Bibliothèque | `<string.h>` | `<string.h>` |
| Objet de recherche | Chaîne C | Zone mémoire |
| Nécessite `'\0'` | Oui | Non |
| S'arrête à `'\0'` | Oui | Non |
| Portée de la recherche | Jusqu'à `'\0'` | Les `n` premiers bytes |
| Paramètre `n` | Non | Oui |
| Peut rechercher des données binaires | Inadapté | Très adapté |
| Valeur de retour | `char *` | `void *` |
| Introuvable | `NULL` | `NULL` |

- `strchr` : Recherche un caractère dans une chaîne
- `memchr` : Recherche un octet dans la mémoire

#### 4. `memchr` 的实现思路

1. 把 s 转换成 unsigned char *
2. 从 i = 0 开始检查 i < n
3. 检查 s\[i] 是否等于 (unsigned char)c:
	- 相等，返回 `&s[i]`
	- 不相等，i++
	- 循环结束，如果还是不相等，返回NULL

memchr(s, c, n) 从 `s` 开始，把内存看成一串 byte，严格检查前 `n` 个 byte，寻找第一个等于 `(unsigned char)c` 的 byte；找到就返回它的地址，找不到就返回 `NULL`.