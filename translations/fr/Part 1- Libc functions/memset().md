`memset` est une **fonction de manipulation de mémoire** très importante en langage C, qui modifie directement chaque octet d'un bloc de mémoire.

#### 1. Prototype

```c
#include <string.h>

void	*memset(void *s, int c, size_t n);
```
Son action peut être simplement comprise comme suit : à partir de s, définir les n octets consécutifs pour qu'ils soient tous égaux aux 8 bits de poids faible de c. 
Les 8 bits de poids faible correspondent, dans la représentation binaire d'un entier, aux 8 bits les plus à droite. La raison pour laquelle memset utilise ces 8 bits est qu'il doit finalement écrire un octet (dont la plage de valeurs va de 0 à 255), et que 1 octet = 8 bits. 
(ps : 1 bit n'a que 2 états : 0 et 1)

Les 3 paramètres de la fonction :
```txt
             memset
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      s         c        n
      │         │        │
      ↓         ↓        ↓
   起始地址    要设置的   设置多少
               字节值     个字节
```
Renvoie l'adresse de départ s de la zone mémoire modifiée, dont le type est `void *`, une adresse mémoire générique. 

`memset` commence à une certaine adresse et modifie n octets. Lorsque n == 0, cela signifie que 0 octet est modifié, rien n'est modifié, ce qui peut être compris comme ne rien faire. 
Attention, n est le nombre d'octets, et non le nombre d'éléments. 

`memset(s, c, n)` signifie : à partir de l'adresse `s`, écrire les `n` octets consécutifs avec les 8 bits de poids faible de `c`, et renvoyer `s`. Les « 8 bits de poids faible » sont les 8 bits les plus à droite de la représentation binaire d'un entier ; si `memset` utilise finalement cette partie, c'est parce qu'il convertit `c` en un `unsigned char`, puis écrit de manière répétée dans la mémoire avec l'octet comme unité.

#### 2. Comprendre les paramètres de la fonction

1. Le 1er paramètre `void *s`
Indique l'adresse de départ de la zone mémoire à manipuler. `void *` est dû au fait que memset ne se soucie pas du type exact que vous lui passez ; il manipule des octets (bytes), et non des types C tels que char, int, double, etc.
Par exemple :
```c
char str[10];
int tab[10];
double values[10];
```
Sont tous possibles :
```c
memset(str, ...);
memset(tab, ...);
memset(values, ...);
```

2. Le 2e paramètre `int c`
Définit n octets à la valeur unsigned char convertie de c. 
Par exemple :
```c
char str[5];

memset(str, 'A', 5);
```
Valeur ASCII de 'A' : 'A' = 65 = 0x41
Par conséquent, 65 converti en hexadécimal donne 0x41, et chaque octet devient 41 41 41 41 41, c'est-à-dire A A A A A.

3. Le 3e paramètre `size_t n`
Indique le nombre d'octets à modifier.
Par exemple :
```c
char str[10];

memset(str, 'A', 3);
```
Signifie :
```txt
第 0 个字节 → A
第 1 个字节 → A
第 2 个字节 → A
```
Ce qui fait un total de 3 octets.

PS : En général, un int fait 4 octets.

#### 3. Utilisations les plus courantes de memset

1. Mettre un tableau à zéro
```c
int tab[100];

memset(tab, 0, sizeof(tab));
```

2. Initialiser une structure
```c
struct person
{
	char	name[50];
	int		age;
};

memset(&p, 0, sizeof(p)); // 把整个结构体占用的字节设置为0
```

3. Vider un tableau de caractères
```c
char buffer[1024];

memset(buffer, 0, sizeof(buffer));
```
Résultat :
```c
buffer[0] = '\0'
buffer[1] = '\0'
buffer[2] = '\0'
...
```

4. Définir un bloc de mémoire à un octet spécifique
```c
char buffer[10];

memset(buffer, 'X', 10);
```
On obtient :
```txt
X X X X X X X X X X
```

```txt
① s 是起始地址
        ↓
② 转成 unsigned char *
        ↓
③ i 从 0 开始
        ↓
④ 每次修改 1 byte
        ↓
⑤ 修改 n 次
        ↓
⑥ 返回原来的 s
```

```c
memset(tab, 1, sizeof(tab));

不是把tab中的每个元素设为1，而是把tab占用的每一个byte都设为0x01
```

#### 4. Comprendre le fonctionnement de la fonction

```txt
                 memset
                    │
                    ↓
             操作 memory
                    │
                    ↓
               按 byte 操作
                    │
                    ↓
             1 byte = 8 bits
                    │
                    ↓
        一个 byte 只有 8 个 bit
                    │
                    ↓
         c 转换成 unsigned char
                    │
                    ↓
            得到一个 byte
                    │
                    ↓
              低 8 位
            
    低8位并不是memset随便选择的，而是因为它最终一次写入的单位就是1个byte, 而这个byte
    在常见平台上是8 bits
```

Exemple : comprendre ces 2 lignes de code
```c
char str[4];

memset(str, 0x12345678, 4);
```
La compréhension se fait en 4 étapes :
Étape 1 : Le 2e paramètre c est 0x12345678.
Étape 2 : Conversion en unsigned char, en ne conservant qu'un seul octet : 0x78.
Étape 3 : Le 3e paramètre n = 4, il faut écrire 4 octets.
```c
byte 0
byte 1
byte 2
byte 3
```
Étape 4 : Tout écrire à 0x78.
```c
┌──────┬──────┬──────┬──────┐
│ 0x78 │ 0x78 │ 0x78 │ 0x78 │
└──────┴──────┴──────┴──────┘
```
C'est ce que fait `memset(str, 0x12345678, 4);`.

PS : Comprendre l'écriture 0x78
0x -> Indique au compilateur que le nombre 78 qui suit est exprimé en hexadécimal. L'écriture 0x est une convention en langage C.
	On peut comprendre `0x` comme : « Le nombre qui suit est représenté en hexadécimal ».
78 -> La partie qui représente réellement la valeur numérique est 78.

[[bzero()]]