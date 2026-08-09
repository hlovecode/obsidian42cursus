`isascii()` 和 `isalpha()`、`isdigit()`、`isalnum()` 一样，都属于**字符分类函数（character classification functions）**, 不过有一个非常重要的区别：`isascii()` 判断的不是"是不是字母或数字"，而是 "这个字符是不是 ASCII 字符".

#### 1. Prototype

```c
#include <ctype.h>

int isascii(int c);
```
它的作用非常简单，判断参数c是否属于ASCII字符范围.
