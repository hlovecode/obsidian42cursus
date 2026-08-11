`strlcat` : **concaténer** une chaîne à la suite d'une chaîne cible

```
strlcat
│││
││└── cat = concatenate
││
│└── l = length-limited
│
└── str = string
```
On peut comprendre strlcat comme *string length-limited concatenate* (concaténation de chaînes avec limitation de longueur).

#### 1. Prototype

```c
#include <string.h>

size_t strlcat(char *dst, const char *src, size_t size);
```
Son rôle est d'ajouter la chaîne `src` à la fin de la chaîne `dst`, tout en utilisant au maximum les `size` octets fournis par `dst`.

Il retourne la longueur de la chaîne complète qu'il a tenté de créer. Si dst et src sont des chaînes normales se terminant par '\0', il retourne `strlen(dst) + strlen(src)`. Attention, il s'agit de la longueur de dst avant la concaténation.

**Attention : le paramètre `size` représente la capacité totale du 1er paramètre `dst`, et non la longueur à ajouter.**

#### 2. Processus de fonctionnement principal de la fonction

1. Trouver la longueur de la chaîne dst.
2. Calculer l'espace restant disponible.
3. Ajouter src.

#### 3. Retourne toujours la longueur complète même en cas d'espace insuffisant

Exemple explicatif :
```c
char dst[10] = "Hello"; // 长度是5
char src[] = " World!!!"; // 长度是9
```
La longueur de la chaîne retournée par `strlcat(...)` est 14, mais dst ne peut en réalité devenir que "Hello Wo" avec une longueur de 8, tout en retournant 14. Puisque la fonction vous indique qu'si l'espace avait été suffisant, elle aurait voulu obtenir une chaîne de longueur 14, on peut ainsi déterminer si une troncature de chaîne s'est produite :
```c
char dst[10] = "Hello";
char src[] = " World!!!";

size_t ret;

ret = strlcat(dst, src, sizeof(dst));

if (ret >= sizeof(dst))
{
	printf("字符串被截断了\n");
}
```
Ici `ret = 14`, `sizeof(dst) = 10`, ce qui indique que la capacité de dst est insuffisante et que src n'a pas été entièrement concaténé.

#### 4. Cas où `size = 0` pour strlcat

Par exemple :
```c
strlcat(dst, src, 0);
```
Cela signifie que la capacité disponible du tampon cible est de 0, donc rien ne peut y être écrit. Cependant, la fonction doit quand même calculer la valeur de retour. Si dst est une chaîne normale :
```c
return strlen(dst) + strlen(src);
```

#### 5. `size` <= longueur actuelle de `dst`

Par exemple :
```c
char dst[20] = "Hello";
char src[] = "World";

strlcat(dst, src, 4);
```
Ici `size = 4, strlen(dst) = 5, size < strlen(dst)`, ce qui signifie que la plage représentée par `size` ne peut même pas contenir la chaîne dst en entier. Dans ce cas, strlcat ne doit pas continuer à accéder à une zone dépassant `size` pour chercher '\0'. La valeur de retour renvoyée dans ce cas particulier est `size + strlen(src)`, c'est-à-dire 4 + 5 = 9. C'est une règle très importante dans l'implémentation de strlcat.

#### 6. Différence entre strlcat et strlcpy

| Fonction                  | Rôle                |
| ------------------------- | ----------------- |
| `strlcpy`                 | Copier une chaîne       |
| `strlcat`                 | Concaténer une chaîne   |
| `strlcpy(dst, src, size)` | `dst ← src`       |
| `strlcat(dst, src, size)` | `dst ← dst + src` |

#### 7. Implémenter soi-même ft_strlcat

Idée principale :
```txt
1. 找 dst 的长度
2. 找 src 的长度
3. 判断 size 是否足够，如果 size <= dst_len：返回 size + src_len
   否则：计算最多可以追加多少字符
   最多追加的字符数 = size - dst_len - 1
4. 如果足够，把 src 全部追加
5. 如果不够，只追加能够容纳的部分
6. 最后添加 '\0'
7. 返回“原 dst 长度 + src 长度”
   
   
                size
                 │
                 ▼
        ┌─────────────────┐
        │   dst 总容量     │
        └─────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
    dst_len          剩余空间
                         │
                         ▼
                  size-dst_len-1
                         │
                         ▼
                    追加 src
```
Dans `strlcat(dst, src, size)`, `size` est **la capacité totale du tampon dst**, tandis que la valeur de retour est **la longueur de l'`dst` d'origine + la longueur de l'`src`**, et non le nombre de caractères réellement ajoutés.