`strlcpy` est une fonction utilisée pour **copier des chaînes de caractères C**

#### 1. Prototype

```c
#include <string.h>

size_t strlcpy(char *dst, const char *src, size_t size);
```
La fonction a pour rôle de copier la chaîne pointée par `src` vers `dst`, en écrivant au maximum `size - 1` caractères, et en garantissant que la chaîne de caractères cible se termine par `'\0'`.
Elle retourne la longueur totale de src, c'est-à-dire strlen(src).

Pourquoi écrit-on au maximum `size - 1` caractères ?
Parce que la dernière position est réservée à '\0', ce qui signifie que dst peut contenir size octets, mais le nombre maximal de caractères est `size - 1`.

```
┌──────────────────────────────┐
│       dst 可以容纳 size       │
├──────────────┬───────────────┤
│ size - 1     │      1        │
│ 字符          │     '\0'      │
└──────────────┴───────────────┘
```

#### 2. Paramètres de la fonction

|Paramètre|Type|Signification|
|---|---|---|
|`dst`|`char *`|Chaîne cible|
|`src`|`const char *`|Chaîne source|
|`size`|`size_t`|Nombre maximal d'octets que `dst` peut contenir|

Notez que le cas où size == 0 est très particulier : dans ce cas, ```
                 strlcpy(dst, src, size)
                              │
                 ┌────────────┴────────────┐
                 │                         │
              size == 0                size > 0
                 │                         │
              不写任何东西            最多写 size-1 字符
                 │                         │
                 │                    最后写 '\0'
                 │
                 └────────────┬────────────┘
                              ↓
                       返回 strlen(src)
``` n'a plus de sens, donc rien ne peut être écrit dans dst, y compris '\0', dst ne sera pas modifié, mais la fonction retourne tout de même strlen(src), c'est-à-dire la longueur de la chaîne source.

```
                 strlcpy(dst, src, size)
                              │
                 ┌────────────┴────────────┐
                 │                         │
              size == 0                size > 0
                 │                         │
              不写任何东西            最多写 size-1 字符
                 │                         │
                 │                    最后写 '\0'
                 │
                 └────────────┬────────────┘
                              ↓
                       返回 strlen(src)
```

###### `strlcpy` copie `src` dans `dst` d'une capacité de `size`, en copiant au maximum `size - 1` caractères, et garantit de se terminer par `size > 0` lors de `'\0'` ; qu'il y ait troncature ou non, elle retourne la longueur totale de `src`
Formule correspondante :
```
size == 0
    → 不写 dst
    → return strlen(src)

size > 0
    → 最多复制 size - 1 个字符
    → dst[size相关位置] = '\0'
    → return strlen(src)
```

**Une méthode pratique pour déterminer s'il y a eu troncature de chaîne :**
```
if (strlcpy(dst, src, sizeof(dst)) >= sizeof(dst))
{
    /* 被截断 */
}
```
`strlcpy(dst, src, sizeof(dst))` retourne `strlen(src)`, si :
`strlen(src) >= sizeof(dst)`, cela indique que `src 的完整字符串长度>= dst 可容纳的空间`

| Fonction        | Objet manipulé | Se soucie de `'\0'` ? |  Limite la taille de la cible ? |
| --------- | ---- | ----------: | --------: |
| `strcpy`  | Chaîne de caractères  |           Oui |         Non |
| `strlcpy` | Chaîne de caractères  |           Oui |         Oui |
| `memcpy`  | Mémoire arbitraire |           Non | Contrôlé via `n` |
```
strcpy  => 复制字符串，不管目标大小

strlcpy => 复制字符串，并限制目标大小

memcpy  => 复制 n 个 byte，根本不管字符串
```

[[memcpy()]]