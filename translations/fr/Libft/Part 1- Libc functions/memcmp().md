`memcmp` compare les contenus des `n` premiers octets de deux blocs de mémoire, et non des chaînes de caractères.
La mémoire est vue comme une suite d'octets, qui sont ensuite comparés un par un.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux zones de mémoire commençant respectivement à `s1` et `s2`, c'est-à-dire le nombre maximal d'octets à comparer.

Valeur de retour :

| Résultat de la comparaison | Valeur de retour de `memcmp` |
| --- | --- |
| Les deux blocs de mémoire sont totalement identiques | `0` |
| Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2` | Inférieur à `0` |
| Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2` | Supérieur à `0` |

La norme C garantit uniquement le signe de la valeur de retour (positif, négatif ou nul), mais pas la valeur exacte. Cela signifie qu'il faut effectuer l'un des tests suivants, et non `memcmp(s1, s2, n) == -1`, car la norme C ne stipule pas qu'elle doit nécessairement retourner -1 :

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

L'exécution de `memcmp(a, b, 3);` compare en réalité :

```c
first byte: 97 == 97

second byte: 98 == 98

third byte: 99 != 100

```

Puisque 99 < 100, par conséquent `memcmp(a, b, 3) < 0`

#### 3. `memcmp` vs `memcpy` vs `memmove`

| Fonction | Rôle |
| --- | --- |
| `memset` | Remplit un bloc de mémoire avec un octet donné |
| `memcpy` | Copie un bloc de mémoire vers un autre |
| `memmove` | Déplace/copie en toute sécurité de la mémoire potentiellement chevauchante |
| `memchr` | Recherche un octet dans la mémoire |
| `memcmp` | Compare deux blocs de mémoire |
| `strlen` | Calcule la longueur d'une chaîne de caractères |
| `strcmp` | Compare des chaînes de caractères |