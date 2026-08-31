If a lowercase English letter is passed `'a'`～`'z'`, convert it to the corresponding uppercase letter `'A'`～`'Z'`; otherwise, return it as is.

#### 1.  Prototype

```c
#include <ctype.h>

int toupper(int c);
```
`toupper()` takes `int`, and also returns `int`

#### 2. Why is the return type int?

`ctype.h` character functions usually require parameters to be able to represent:
1. a `unsigned char` value
2. or the special value `EOF`, `EOF` is generally defined as a negative `int` value
Therefore, int is used to pass characters

[[tolower()]]

---

## 中文原文

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
2. 或者特殊值 `EOF`, `EOF` 一般定义为一个负的 `int` 值
因此使用 int 来传递字符

[[tolower()]]
