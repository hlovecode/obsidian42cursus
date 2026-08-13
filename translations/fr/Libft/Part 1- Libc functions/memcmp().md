`memcmp` compare le contenu des `n` premiers octets de deux blocs mémoire, et non des chaînes de caractères.
Il traite la mémoire comme une séquence d'octets et les compare un par un.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux zones mémoire commençant respectivement à `s1` et `s2`, c'est-à-dire le nombre maximal d'octets à comparer.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour de `memcmp`|
|---|---|
|Les deux blocs mémoire sont totalement identiques|`0`|
|Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2`|Inférieur à `0`|
|Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2`|Supérieur à `0`|

La norme C garantit seulement le signe de la valeur de retour ou zéro, mais ne garantit pas la valeur exacte retournée. En d'autres termes, il faut effectuer l'un des tests suivants plutôt que `memcmp(s1, s2, n) == -1`, car la norme C ne stipule pas qu'elle doit nécessairement retourner -1 :

```c
if (memcmp(s1, s2, n) > 0)

if (memcmp(s1, s2, n) == 0)

if (memcmp(s1, s2, n) < 0)
```

#### 2. `memcmp` compare des octets

Exemple :

```c
char a[] = "abc";
char b[] = "abd";
```

La mémoire peut en fait être comprise comme :

```c
a:

address
 ↓
+----+----+----+----+
| a  | b  | c  | \0 |
+----+----+----+----+
 97   98   99    0
 
 
 b:
 
+----+----+----+----+
| a  | b  | d  | \0 |
+----+----+----+----+
 97   98  100    0

```