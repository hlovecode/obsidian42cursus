`isalnum()` is a very basic and commonly used **character classification function** in the C standard library `<ctype.h>`, used to determine whether a character is an alphanumeric character (a letter or a digit).

#### 1. Prototype

```c
#include <ctype.h>

int isalnum(int c);
```
It checks whether:
```txt
A-Z
a-z
0-9
```
- If it is a letter or a digit, it returns a non-zero value.
- If it is not, it returns 0.

**The relationship between `isalnum` and `isalpha`, `isdigit`**:
```txt
isalnum 判断是不是字母或数字
   │
   ├── isalpha 只判断是不是字母
   │     └── A-Z / a-z
   │
   └── isdigit 只判断是不是数字
         └── 0-9
```

#### 2. isalnum does not check for the underscore _, nor does it handle negative numbers

```c
isalnum('_') // 不是字母和数字，返回0
isalnum(-100); // 错误
```

[[isalpha()]]
[[isdigit()]]