Si l'argument transmis est une lettre minuscule `'a'`～`'z'`, elle est convertie en la lettre majuscule correspondante `'A'`～`'Z'` ; sinon, elle est renvoyée telle quelle.

#### 1.  Prototype

```c
#include <ctype.h>

int toupper(int c);
```
`toupper()` prend `int` en paramètre et retourne `int`

#### 2. Pourquoi le type de retour est-il int ?

Les fonctions de manipulation de caractères dans `ctype.h` exigent généralement que les arguments puissent représenter :
1. Une valeur `unsigned char`
2. Ou la valeur spéciale `EOF`, `EOF` étant généralement défini comme une valeur `int` négative
Par conséquent, on utilise int pour passer les caractères.

[[tolower()]]