Si le caractère passé est une lettre alphabétique minuscule `'a'`～`'z'`, elle est convertie en sa majuscule correspondante `'A'`～`'Z'` ; sinon, elle est renvoyée telle quelle.

#### 1. Prototype

```c
#include <ctype.h>

int toupper(int c);
```
`toupper()` prend un `int` en argument et retourne également un `int`

#### 2. Pourquoi le type de retour est-il int ?

Les fonctions sur les caractères de `ctype.h` exigent généralement que le paramètre puisse représenter :
1. Une valeur de type `unsigned char`
2. Ou la valeur spéciale `EOF`, `EOF` étant généralement défini comme une valeur entière négative `int`
Par conséquent, on utilise int pour passer les caractères.

[[tolower()]]