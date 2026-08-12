strrchr recherche la dernière occurrence d'un caractère dans une chaîne.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais en renvoyant la dernière occurrence du caractère.
L'implémentation concrète peut parcourir la chaîne du début vers la fin, ou de la fin vers le début.

#### 2. Différence entre `strrchr` et `strchr`

Par exemple : la lettre « o » apparaît 2 fois dans « hello world »

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr` : recherche le caractère de gauche à droite et renvoie la première occurrence.
 - `strrchr` : recherche de gauche à droite, mais renvoie la dernière occurrence.

#### 3. Valeur de retour de `strrchr`

Le type de la valeur de retour est `char *` ; elle renvoie l'adresse du caractère trouvé, ou NULL si le caractère n'est pas trouvé.

Une caractéristique importante de `strrchr` est qu'il recherche également '\0', c'est-à-dire qu'il renvoie l'adresse du caractère de fin de chaîne '\0'.