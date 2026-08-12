`isprint()` et les fonctions `isalpha()`, `isdigit()`, `isalnum()`, `isascii()` que vous avez étudiées précédemment font partie du même groupe de **fonctions de classification des caractères C (character classification functions)**, utilisées pour déterminer si un caractère est un **caractère imprimable (printing character)**.

#### 1. Prototype
```c
#include <ctype.h>

int isprint(int c);
```
Son rôle est de déterminer si le paramètre c est un caractère qui peut être affiché normalement.
- S'il s'agit d'un caractère imprimable, retourne une valeur non nulle.
- Sinon, retourne 0.

#### 2. Qu'est-ce qu'un caractère imprimable ?

Les caractères ASCII sont grossièrement divisés en :
```txt
0 ~ 31     控制字符
32 ~ 126   可打印字符
127        DEL
```
Par conséquent, la plage de vérification de `isprint()` est de 32 à 126, c'est-à-dire 32 <= paramètre c <= 126.

#### 3. L'espace ' ' est également un caractère imprimable
Parce que la valeur ASCII de l'espace est 32, bien qu'il n'ait pas de représentation graphique, il peut être matérialisé sur un terminal ou un écran.

#### 4. Pourquoi les codes 0 à 31 de l'ASCII ne sont-ils pas imprimables ?
Les codes 0 à 31 sont des caractères de contrôle. Leur rôle n'est pas d'afficher un symbole ordinaire, mais de contrôler le terminal, le curseur, les sauts de ligne, etc.