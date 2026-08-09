`isdigit()` 是 C 标准库 `<ctype.h>` 中用于**判断一个字符是否为十进制数字字符**的函数.
`isdigit()` 判断的范围严格就是：
```c
'0' '1' '2' '3' '4' '5' '6' '7' '8' '9'
```
也就是ASCII：48 ~ 57
##### 1. Prototype
```c
#include <ctype.h> 

int isdigit(int c);
```
它的作用非常简单：判断c是否表示字符 '0' 到 '9' 中的一个.
返回值：
- 是数字字符 '0' ~ '9' 则返回非0
- 如果不是，则返回0
例如：
```c
isdigit('0');   // 非 0
isdigit('5');   // 非 0
isdigit('9');   // 非 0

isdigit('a');   // 0
isdigit('A');   // 0
isdigit(' ');   // 0
isdigit('-');   // 0
isdigit('\n');  // 0
```

##### 2. `isdigit()` 判断的是“字符”，不是“数字”
`isdigit()` 一次只能判断**一个字符**.

例如：
```c
isdigit('123') // 错误， 一次只能判断一个字符
```
正确：
```c
isdigit('1')
isdigit('2')
isdigit('3')
```
如果要判断整个字符串是不是由数字组成的，需要逐个字符检查：
```c
int i;

i = 0;
while (str[i])
{
    if (!isdigit(str[i]))
        return (0);
    i++;
}
return (1);
```

**isdigit()不判断负号，也不判断小数点**，只要不是数字字符，都返回0.