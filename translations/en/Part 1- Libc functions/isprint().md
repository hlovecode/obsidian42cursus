`isprint()` and `isalpha()`, `isdigit()`, `isalnum()`, `isascii()` which you learned earlier belong to the same group of **C character classification functions**, used to determine whether a character is a **printing character**.

#### 1. Prototype
```c
#include <ctype.h>

int isprint(int c);
```
Its function is to determine whether the parameter c is a character that can be normally printed and displayed.
- If it is a printable character, it returns a non-zero value.
- If not, it returns 0.

#### 2. What is a printable character?

ASCII characters are roughly divided into:
```txt
0 ~ 31     控制字符
32 ~ 126   可打印字符
127        DEL
```
Therefore, the judgment range of `isprint()` is 32 to 126, i.e., 32 <= parameter c <= 126.

#### 3. The space ' ' is also a printable character
Because the ASCII value of a space is 32, although it has no graphical shape, it can be represented on a terminal or screen.

#### 4. Why can't 0 ~ 31 in ASCII be printed?
0 ~ 31 are control characters. Their function is not to display a regular symbol, but to control terminals, cursors, newlines, etc.