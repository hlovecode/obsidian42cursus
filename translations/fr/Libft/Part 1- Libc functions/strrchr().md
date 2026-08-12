strrchr recherche la dernière occurrence d'un certain caractère dans une chaîne.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais de renvoyer la position de la dernière apparition du caractère.
L'implémentation concrète peut balayer la chaîne de gauche à droite ou de droite à gauche.

#### 2. Différence entre `strrchr` et `strchr`

Par exemple : la lettre « o » apparaît 2 fois dans « hello world »

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr` : recherche le caractère de gauche à droite et renvoie la position de sa première occurrence.
 - `strrchr` : recherche de gauche à droite, mais renvoie la position de la dernière occurrence.

#### 3. Valeur de retour de `strrchr`

Le type de la valeur de retour est `char *`, qui renvoie l'adresse du caractère trouvé, ou NULL si le caractère n'est pas trouvé.

Une caractéristique importante de `strrchr` est qu'il recherche également '\0', c'est-à-dire qu'il renvoie l'adresse du caractère de fin de chaîne '\0'.

#### 4. Le cas d'usage courant de `strrchr` est « l'obtention de l'extension de fichier »

Exemple 1 : `strrchr` est très couramment utilisé lors du traitement de chemins de fichiers et de noms de fichiers.

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

Le pointeur de résultat p pointe vers `.txt` de document.txt, donc :

```c
printf("%s\n", p); // .txt
```

Exemple 2 : Regardons un autre exemple de chemin, si nous voulons trouver le dernier `/`, nous pouvons faire :

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p pointe vers le dernier `/` de la chaîne « /Users/lee/project/main.c », alors :

```c
printf("%s\n", p + 1);
```

On obtient `main.c`