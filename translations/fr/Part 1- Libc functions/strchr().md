`strchr` a un rôle très simple : il cherche la première occurrence d'un caractère donné dans une chaîne de caractères, du début à la fin.

#### Prototype

```c
#include <string.h>

char *strchr(const char *s, int c);
```
`strchr` **ne retourne pas le caractère lui-même**, mais : 
- Si le caractère est trouvé, il retourne son **adresse** dans la chaîne. 
- Si le caractère n'est pas trouvé, il retourne `NULL` (0). 

`strchr` lit la chaîne de caractères, mais n'en modifie pas le contenu.

```
从字符串的第一个字符开始
        ↓
比较当前字符和 c
        ↓
	   相同？
 ┌──────┴──────┐
是             否
↓              ↓
返回当前地址    移动到下一个字符
               ↓
            继续比较
            
直到：
1. 找到目标字符
2. 遇到 `'\0'`
```