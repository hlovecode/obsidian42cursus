`isascii()`, tout comme `isalpha()`, `isdigit()` et `isalnum()`, fait partie des **fonctions de classification de caractères (character classification functions)**, mais il y a une différence très importante : `isascii()` ne teste pas si un caractère est « une lettre ou un chiffre », mais si « ce caractère est un caractère ASCII ».

#### 1. Prototype

```c
#include <ctype.h>

int isascii(int c);
```
Son rôle est très simple : déterminer si le paramètre c appartient à la plage des caractères ASCII.
La plage ASCII va de 0 à 127 (128 valeurs), c'est-à-dire de 0x00 à 0x7F en hexadécimal, soit :
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
Par conséquent, 0 <= paramètre c <= 127 correspond à l'ASCII.

#### 2. ASCII n'est pas synonyme de caractère imprimable, il comprend également un grand nombre de caractères non imprimables

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

`isascii()` est souvent utilisé pour vérifier si une chaîne de caractères ne contient que des caractères ASCII, en vérifiant simplement si la valeur numérique se situe dans la plage ASCII, c'est-à-dire de 0 à 127.