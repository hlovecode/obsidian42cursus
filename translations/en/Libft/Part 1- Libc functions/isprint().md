`isprint()` and the `isalpha()`, `isdigit()`, `isalnum()`, and `isascii()` you learned previously belong to the same group of **C character classification functions**, used to determine whether a character is a **printing character**.

#### 1. Prototype
```c
#include <ctype.h>

int isprint(int c);
```
Its purpose is to determine whether the parameter c is a character that can be normally printed and displayed.
- If it is a printable character, it returns a non-zero value.
- If it is not, it returns 0.

#### 2. What is a printable character?

ASCII characters are roughly divided into:
```txt
0 ~ 31     控制字符
32 ~ 126   可打印字符
127        DEL
```
Therefore, the judgment range of `isprint()` is 32 to 126, which is 32 <= parameter c <= 126.

#### 3. The space character ' ' is also a printable character
Because the ASCII value of a space is 32; although it has no graphical representation, it can occupy space on a terminal or screen.

#### 4. Why are 0 ~ 31 in ASCII non-printable?
0 ~ 31 are control characters. Their function is not to display ordinary symbols, but to control terminals, cursors, newlines, etc.