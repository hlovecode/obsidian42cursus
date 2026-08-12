`isdigit()` est une fonction de la bibliothèque standard C `<ctype.h>` utilisée pour **déterminer si un caractère est un chiffre décimal**.
`isdigit()` évalue strictement la plage suivante :
```c
'0' '1' '2' '3' '4' '5' '6' '7' '8' '9'
```
C'est-à-dire les codes ASCII : 48 à 57
##### 1. Prototype
```c
#include <ctype.h> 

int isdigit(int c);
```
Son rôle est très simple : déterminer si c représente l'un des caractères '0' à '9'.
Valeur de retour :
- Renvoie une valeur non nulle s'il s'agit d'un caractère chiffre '0' ~ '9'
- Renvoie 0 dans le cas contraire
Par exemple :
```c
isdigit('0');   // 非 0
isdigit('5');   // 非 0
isdigit('9');   // 非 0

isdigit('a');   // 0
isdigit('A');   // 0
isdigit(' ');   // 0
isdigit('-');   // 0
isdigit('\n');  // 0
```

##### 2. `isdigit()` évalue un « caractère », pas un « nombre »
`isdigit()` évalue **un seul caractère** à la fois.

Par exemple :
```c
isdigit('123') // 错误， 一次只能判断一个字符
```
Correct :
```c
isdigit('1')
isdigit('2')
isdigit('3')
```
Pour vérifier si une chaîne de caractères entière est composée de chiffres, il est nécessaire de l'examiner caractère par caractère :
```c
int i;

i = 0;
while (str[i])
{
    if (!isdigit(str[i]))
        return (0);
    i++;
}
return (1);
```

**isdigit() ne prend pas en compte le signe moins ni le point décimal** ; tout ce qui n'est pas un chiffre renvoie 0.

[[isalnum()]]