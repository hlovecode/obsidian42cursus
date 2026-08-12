<<<<<<< HEAD
Si l'argument transmis est une lettre minuscule `'a'`～`'z'`, elle est convertie en la lettre majuscule correspondante `'A'`～`'Z'` ; sinon, elle est renvoyée telle quelle.
=======
Si l'argument transmis est une lettre minuscule `'a'`～`'z'`, la convertir en la lettre majuscule correspondante `'A'`～`'Z'` ; sinon, le renvoyer tel quel.
>>>>>>> origin/main

#### 1. Prototype

```c
#include <ctype.h>

int toupper(int c);
```
<<<<<<< HEAD
`toupper()` prend en paramètre un `int` et renvoie également un `int`

#### 2. Pourquoi le type de retour est-il int ?

Les fonctions de caractères dans `ctype.h` exigent généralement que les arguments puissent représenter :
1. Une valeur `unsigned char`
2. Ou la valeur spéciale `EOF`, `EOF` étant généralement défini comme une valeur `int` négative
Par conséquent, on utilise int pour passer les caractères.
=======
`toupper()` prend un `int` en argument et renvoie également un `int`

#### 2. Pourquoi le type de retour est-il int ?

Les fonctions sur les caractères de `ctype.h` exigent généralement que le paramètre puisse représenter :
1. Une valeur `unsigned char`
2. Ou la valeur spéciale `EOF`, `EOF` étant généralement défini comme une valeur `int` négative
C'est pourquoi on utilise int pour passer les caractères.
>>>>>>> origin/main

[[tolower()]]