`tolower()` 是 C 语言中用于**把大写英文字母转换成小写字母**的函数。它和 `toupper()` 是一对相反的函数. 

不过有一个非常重要的细节：**`tolower()` 不一定真的会“转换”输入，它也可能直接返回原来的字符**

#### Prototype

```c
#include <ctype.h>

int tolower(int c);
```
