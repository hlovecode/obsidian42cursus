strrchr recherche la dernière occurrence d'un caractère dans une chaîne de caractères.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais en renvoyant la dernière occurrence du caractère.
L'implémentation spécifique peut parcourir la chaîne du début à la fin, ou de la fin vers le début.

#### 2. `strrchr` et `strchr`