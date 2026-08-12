`bzero` est une fonction utilisée pour **définir une zone de mémoire entière à `0`**.

#### 1. Prototype
```c
#include <strings.h>
 
void	bzero(void *s, size_t n);
```
Son rôle est de commencer à partir de l'adresse mémoire pointée par `s`, et de définir les `n` octets consécutifs à `0`.
Elle n'a pas de valeur de retour, elle effectue simplement une opération de modification de la mémoire.

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

Le sens de la fonction est de commencer à partir de l'adresse `s`, d'accéder à `n` octets consécutifs, et d'écrire chaque octet à `0x00`

#### 2. Comprendre les paramètres de la fonction

1. `size_t n` représente l'adresse d'un objet de type quelconque.

2. `size_t n` représente le nombre d'octets à effacer (mettre à zéro).
Attention, il ne s'agit pas du nombre d'éléments, mais du nombre d'octets.

**Le sens fondamental de la fonction est `bzero(起始地址，字节数量)`**

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
Mais cela efface seulement les 5 premiers octets. En supposant qu'un `int` = 4 octets, alors :
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
L'exécution de `bzero(tab, 5);` donnera seulement :
```c
00 00 00 00 00
^^^^^^^^^^^^^^
  5 bytes
```
C'est-à-dire que cela efface complètement uniquement `tab[0]`, puis efface le premier octet de `tab[1]`, ce qui n'est pas l'effet escompté.
Par conséquent, la bonne écriture est :
```c
bzero(tab, sizeof(tab));
```

#### 4. Utilisation de la fonction

Son utilisation la plus typique est de mettre la mémoire à zéro.

Cependant, notez que cette fonction n'est pas une « suppression de données », elle ne libère pas la mémoire, elle modifie seulement le contenu de la mémoire spécifiée. Bien que la mémoire soit mise à zéro (définie à 0), elle reste occupée.

[[memset()]]