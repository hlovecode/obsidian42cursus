`bzero` est une fonction utilisée pour **remplir une zone mémoire avec la valeur `0`**.

#### 1. Prototype
```c
#include <strings.h>
 
void	bzero(void *s, size_t n);
```
Son rôle est de définir les `n` octets consécutifs, à partir de l'adresse mémoire pointée par `s`, à la valeur `0`.
Elle ne renvoie aucune valeur, elle effectue simplement une opération de modification de la mémoire.

Exemple explicatif :
```c
char str[10] = "abcdef";

bzero(str, 3);
```

```txt
原来的内存大概是：
地址       内容
1000       'a'
1001       'b'
1002       'c'
1003       'd'
1004       'e'
1005       'f'
1006       '\0'
...

执行bzero(str, 3)以后：
地址       内容
1000       0
1001       0
1002       0
1003       'd'
1004       'e'
1005       'f'
1006       '\0'
...
即从 `str` 开始的3个byte被清零
```

La fonction signifie que, à partir de l'adresse `s`, on accède consécutivement à `n` octets (bytes), et on écrit la valeur `0x00` dans chaque octet.

#### 2. Comprendre les paramètres de la fonction

1. `void *` représente l'adresse d'un objet de type quelconque.

2. `size_t n` représente le nombre d'octets à mettre à zéro.
Attention, il ne s'agit pas du nombre d'éléments, mais bien du nombre d'octets.

**Le sens fondamental de la fonction est `bzero(起始地址，字节数量)`.**

#### 3. Attention particulière : bzero fonctionne par octet
Exemple :
```c
int tab[5];

bzero(tab, 5);
```
Ce n'est pas :
```c
tab[0] = 0
tab[1] = 0
tab[2] = 0
tab[3] = 0
tab[4] = 0
```
Mais cela met uniquement à zéro les 5 premiers octets. En supposant qu'un int = 4 octets, alors :
```c
tab:

byte 0 ──┐
byte 1   │ tab[0]
byte 2   │
byte 3 ──┘

byte 4 ──┐
byte 5   │ tab[1]
byte 6   │
byte 7 ──┘
...
```
L'exécution de bzero(tab, 5); donnera seulement :
```c
00 00 00 00 00
^^^^^^^^^^^^^^
  5 bytes
```
C'est-à-dire qu'il efface complètement `tab[0]`, puis efface le premier octet de `tab[1]`, ce qui n'est pas l'effet attendu.
Par conséquent, la bonne écriture est :
```c
bzero(tab, sizeof(tab));
```

#### 4. Utilisation de la fonction

Son usage le plus typique est de mettre la mémoire à zéro.

Cependant, notez que cette fonction n'est pas une "suppression de données", elle ne libère pas la mémoire, elle modifie seulement le contenu de la mémoire spécifiée. Bien que la mémoire soit mise à zéro, ce qui signifie simplement que la zone mémoire est réglée à 0, la mémoire reste occupée.

[[memset()]]