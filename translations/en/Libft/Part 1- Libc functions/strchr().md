`strchr` serves a very simple purpose: it searches for the first occurrence of a specific character in a string from beginning to end.

#### Prototype

```c
#include <string.h>

char *strchr(const char *s, int c);
```
`strchr` **does not return the character itself**, but instead returns: 
- If the character is found, it returns the **address** of that character in the string. 
- If the character is not found, it returns NULL (0). 

`strchr` reads the string, but does not modify its contents.

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