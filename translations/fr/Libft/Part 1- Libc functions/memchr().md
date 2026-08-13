`memchr` recherche un octet spécifique dans les `n` premiers octets d'un bloc de mémoire, sans se soucier du caractère `'\0'`.
`memchr` recherche l'octet `byte` et non un caractère, mais comme un caractère occupe généralement un octet dans les chaînes ASCII ordinaires, il semble que l'on recherche un caractère.
Cette fonction lit uniquement la mémoire et ne la modifie pas.

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Son rôle est de commencer à partir de la zone mémoire `s`, d'examiner les `n` premiers octets et de rechercher le premier octet dont la valeur est égale à `(unsigned char)c`.

Valeur de retour :

- En cas de succès, retourne un pointeur vers cet octet.
- Si le caractère n'est pas trouvé, retourne `NULL`.

#### 2.