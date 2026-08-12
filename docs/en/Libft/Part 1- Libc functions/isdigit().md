`isdigit()` is a function in the C standard library `<ctype.h>` used to **determine whether a character is a decimal digit character**.
The range checked by `isdigit()` is strictly:
```c
'0' '1' '2' '3' '4' '5' '6' '7' '8' '9'
```
Which is ASCII: 48 ~ 57
##### 1. Prototype
```c
#include <ctype.h> 

int isdigit(int c);
```
Its function is very simple: it determines whether `c` represents one of the characters '0' through '9'.
Return value:
- Returns non-zero if it is a digit character '0' ~ '9'.
- Returns zero if it is not.
For example:
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

##### 2. `isdigit()` checks for "characters", not "numbers"
`isdigit()` can only check **one character** at a time.

For example:
```c
isdigit('123') // 错误， 一次只能判断一个字符
```
Correct:
```c
isdigit('1')
isdigit('2')
isdigit('3')
```
If you want to determine whether an entire string consists of digits, you need to check it character by character:
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

**`isdigit()` does not check for negative signs, nor does it check for decimal points**; anything that is not a digit character will return 0.

[[isalnum()]]