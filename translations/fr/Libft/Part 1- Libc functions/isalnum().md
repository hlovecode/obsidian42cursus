`isalnum()` est une **fonction de classification de caractères** très fondamentale et très couramment utilisée dans la bibliothèque standard C `<ctype.h>`, servant à déterminer si un caractère est une lettre ou un chiffre.

#### 1. Prototype

```c
#include <ctype.h>

int isalnum(int c);
```
Elle détermine :
```txt
A-Z
a-z
0-9
```
- Si c'est une lettre ou un chiffre, elle retourne une valeur non nulle.
- Sinon, elle retourne 0.

**Relation entre `isalnum`, `isalpha` et `isdigit`** :
```txt
isalnum 判断是不是字母或数字
   │
   ├── isalpha 只判断是不是字母
   │     └── A-Z / a-z
   │
   └── isdigit 只判断是不是数字
         └── 0-9
```

#### 2. isalnum ne prend pas en compte le tiret bas _, ni les nombres négatifs

```c
isalnum('_') // 不是字母和数字，返回0
isalnum(-100); // 错误
```

[[isalpha()]]
[[isdigit()]]