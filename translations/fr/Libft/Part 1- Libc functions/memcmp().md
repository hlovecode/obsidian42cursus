`memcmp` compare le contenu des premiers `n` octets (bytes) de deux blocs de mémoire, et non les chaînes de caractères.
La mémoire est considérée comme une suite d'octets, qui sont ensuite comparés un par un.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux zones mémoire commençant respectivement par `s1` et `s2`, c'est-à-dire de comparer au maximum un certain nombre d'octets.

Valeur de retour :

|Résultat de la comparaison|Valeur de retour de `memcmp`|
|---|---|
|Les deux blocs de mémoire sont entièrement identiques|`0`|
|Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2`|Inférieur à `0`|
|Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2`|Supérieur à `0`|

La norme C garantit uniquement le signe de la valeur de retour (positif, négatif ou nul) et non sa valeur exacte. Par conséquent, il convient de tester l'un des cas suivants plutôt que d'utiliser `memcmp(s1, s2, n) == -1`, car la norme C ne garantit pas de renvoyer obligatoirement -1 :

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

La mémoire peut en réalité être représentée ainsi :

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

L'exécution de `memcmp(a, b, 3);` compare en fait :

```c
first byte: 97 == 97

second byte: 98 == 98

third byte: 99 != 100

```

Puisque 99 < 100, par conséquent `memcmp(a, b, 3) < 0`

#### 3. `memcmp` vs `memcpy` vs `memmove`

| Fonction    | Action              |
| --------- | --------------- |
| `memset`  | Remplit un bloc de mémoire avec un octet donné |
| `memcpy`  | Copie un bloc de mémoire vers un autre bloc   |
| `memmove` | Déplace/copie en toute sécurité de la mémoire potentiellement chevauchante |
| `memchr`  | Recherche un octet dans la mémoire   |
| `memcmp`  | Compare deux blocs de mémoire          |

Le point commun de cette famille de fonctions est de traiter les données comme des octets bruts (raw bytes) et non comme des « chaînes de caractères ».

#### 4. `memcmp` vs `strcmp`

| Critère de comparaison | `memcmp`                                                | `strcmp`                                      |
| ------------------- | ------------------------------------------------------- | --------------------------------------------- |
| **Prototype**       | `int memcmp(const void *s1, const void *s2, size_t n);` | `int strcmp(const char *s1, const char *s2);` |
| **Rôle**            | Compare les `n` premiers **octets (bytes)** de deux blocs de mémoire                             | Compare deux **chaînes de caractères (strings)**         |
| **Nécessite `n`** | **Oui**, `n` spécifie le nombre d'octets à comparer                             | **Non**                                         |
| **Exige `\0`**     | **Non**                                                 | **Exige que la chaîne se termine par `\0`**           |
| **Condition d'arrêt** | Avoir comparé `n` octets, ou rencontre du premier octet différent | Rencontre du premier caractère différent, ou de `\0` |
| **Objets comparés** | N'importe quelle donnée en mémoire                      | Chaînes de caractères C                         |
| **Peut comparer des données binaires** | **Oui**                                                | **Inadapté**                                    |
| **Traite `\0` comme un terminateur spécial** | **Non**, `\0` est simplement un octet ordinaire | **Oui**, `\0` marque la fin de la chaîne |
| **Renvoie `0`** | Les `n` premiers octets sont tous identiques            | Les deux chaînes ont un contenu identique              |
| **Renvoie `< 0`** | Dans le premier octet différent, `s1` est inférieur à `s2` | Dans le premier caractère différent, `s1` est inférieur à `s2` |
| **Renvoie `> 0`** | Dans le premier octet différent, `s1` est supérieur à `s2` | Dans le premier caractère différent, `s1` est supérieur à `s2` |
| **Utilisation typique** | Comparaison de tableaux, de mémoire brute dans des structures, de données binaires | Comparaison de noms d'utilisateur, de mots, de phrases, etc. |
| **Exemple**         | `memcmp(a, b, 10)`                                      | `strcmp("abc", "abd")`                        |

`memcmp` compare un « nombre spécifié d'octets en mémoire », tandis que `strcmp` compare des « chaînes de caractères terminées par `\0` ».