`isascii()` and `isalpha()`, `isdigit()`, `isalnum()` all belong to **character classification functions**, but there is a very important difference: `isascii()` does not check whether "it is a letter or a digit", but rather "whether this character is an ASCII character".

#### 1. Prototype

```c
#include <ctype.h>

int isascii(int c);
```
Its function is very simple: it checks whether the parameter c falls within the ASCII character range.
The ASCII range is 0 to 127 (128 values), which is hexadecimal 0x00 to 0x7F, namely:
```txt
0
│
├── 0 ~ 31       控制字符
│
├── 32            空格 ' '
│
├── 33 ~ 47      标点符号
│
├── 48 ~ 57      '0' ~ '9'
│
├── 58 ~ 64      标点符号
│
├── 65 ~ 90      'A' ~ 'Z'
│
├── 91 ~ 96      标点符号
│
├── 97 ~ 122     'a' ~ 'z'
│
├── 123 ~ 126    标点符号
│
└── 127           DEL
```
Therefore, 0 <= parameter c <= 127 means it is ASCII.

#### 2. ASCII does not equal printable characters; it also includes a large number of non-printable characters

```txt
ASCII
  │
  ├── 可打印字符
  │
  └── 不可打印控制字符
```

```txt
             isascii
                │
       ┌────────┴────────┐
       │                 │
      ASCII            非 ASCII
       ├── 字母
       ├── 数字
       ├── 标点
       ├── 空格
       └── 控制字符
```

`isascii()` is often used to check whether a string contains only ASCII characters by simply checking whether the numerical values fall within the ASCII range, i.e., 0 to 127.