#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
它的作用非常简单，计算字符串中的字符数量，但不包括结尾的`'\0`. 

#### 2. 为什么不计算'\0' ?

C语言中的字符串不是一种独立的数据类型，实际上是一串char. 
'\0' 的作用是告诉C，字符串到这里结束. 
如果逻辑上的字符串长度是5，实际占用的字符数组空间是6.

`strlen()` 只读取字符串，不会修改字符串内容.
函数参数必须指向一个以'\0'结尾的有效C字符串.

strlen("") 是一个空字符串，实际上是'\0'，函数返回0.
注意：空字符串不是没有内存，而是有一个'\0'.

strlen(NULL)非法，是undefined behavior, 因为strlen会尝试访问一个根本没有有效的字符串，因此不要写:
```c
char *str = NULL;
strlen(str);
```
也不要使用strlen来判断str是否是NULL，不要写：
```c
if (strlen(str) == 0) 来判断 str == NULL
```
正确的是：
```c
if (str == NULL)
{
	/* NULL */
	...
}
else if (strlen(str) == 0)
{
	/* empty string */
	...
}
```

#### 3. 类型 size_t

它是一个无符号整数类型`unsigned int` 或 `unsigned long`, 由`<stddef.h>` 声明定义，是用作数组下标任意整数数据对象的最安全的类型, 不必担心小的数组会随着程序的变化而演变为很大的数组.

使用`size_t` 时，下标算术永远都不会溢出，在程序中所有对数组下标或地址进行算术操作的地方，都应该使用`size_t`类型，缺点是不能使用负值. 

`size_t` 是 C 标准定义的一个无符号整数类型，专门用于表示：
- 对象大小
- 数组大小
- 内存大小
- 字节数量


## GitHub Actions 测试

这是一次 GitHub Actions 自动翻译测试。
