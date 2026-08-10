如果传入的是小写英文字母 `'a'`～`'z'`，就把它转换成对应的大写字母 `'A'`～`'Z'`；否则原样返回.

#### 1.  Prototype

```c
#include <ctype.h>

int toupper(int c);
```
`toupper()` 接收的是 `int`，返回的也是 `int`

#### 2. 为什么返回类型是 int ?

`ctype.h` 中的字符函数通常要求参数能够表示：
1. 一个 `unsigned char` 的值
2. 或者特殊值 `EOF`
因此使用 int 来传递字符