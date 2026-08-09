`isprint()` 和你前面学习的 `isalpha()`、`isdigit()`、`isalnum()`、`isascii()` 属于同一组 **C 字符分类函数 (character classification functions)**, 用来判断一个字符是否是**可打印字符(printing character)**.

#### 1. Prototype
```c
#include <ctype.h>

int isprint(int c);
```
它的作用是判断参数c是否是一个可以正常显示出来的字符.
- 如果是可打印字符，返回非0
- 如果不是，则返回0

#### 2. 什么是可打印字符？

ASCII字符大致分成：
```txt
0 ~ 31     控制字符
32 ~ 126   可打印字符
127        DEL
```
所以`isprint()`的判断范围是32 ~ 126， 即32 <= 参数c <= 126

#### 3. 空格' '也是可打印字符
因为空格的ASCII值是32，它虽然没有图形，但在终端或屏幕上是可以表现出来的.

#### 4. ASCII中为什么0 ~ 31不能打印
0 ~ 31 是控制字符，它们的作用不是显示一个普通符号，而是控制终端，光标，换行deng