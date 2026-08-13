`memcmp` compare le contenu des premiers `n` octets (bytes) de deux blocs de mémoire, et non des chaînes de caractères.
La mémoire est considérée comme une suite d'octets, comparés un par un.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Son rôle est de comparer les `n` premiers octets des deux zones mémoire commençant respectivement à `s1` et `s2`, c'est-à-dire de comparer au maximum ce nombre d'octets.

Valeur de retour :

| Résultat de la comparaison | Valeur de retour de `memcmp` |
|---|---|
| Les deux blocs de mémoire sont entièrement identiques | `0` |
| Le premier octet différent dans `s1` est **inférieur** à l'octet correspondant dans `s2` | Inférieur à `0` |
| Le premier octet différent dans `s1` est **supérieur** à l'octet correspondant dans `s2` | Supérieur à `0` |

La norme C garantit seulement le signe de la valeur de retour (positif, négatif ou nul) et non sa valeur exacte. Par conséquent, il convient d'effectuer l'une des vérifications ci-dessous, et non `memcmp(s1, s2, n) == -1`, car la norme C ne stipule pas qu'elle doit nécessairement retourner -1 :

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

La mémoire peut en réalité être interprétée comme suit :

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

L'exécution de `memcmp(a, b, 3);` compare en pratique :

```c
first byte: 97 == 97

second byte: 98 == 98

third byte: 99 != 100

```

Puisque 99 < 100, par conséquent `memcmp(a, b, 3) < 0`

#### 3. `memcmp` vs `memcpy` vs `memmove`

| Fonction | Action |
| --- | --- |
| `memset` | Remplit un bloc de mémoire avec un octet spécifique |
| `memcpy` | Copie un bloc de mémoire vers un autre |
| `memmove` | Déplace/copie en toute sécurité de la mémoire potentiellement chevauchante |
| `memchr` | Recherche un octet dans la mémoire |
| `memcmp` | Compare deux blocs de mémoire |
Le point commun de ce groupe de fonctions est qu'elles considèrent les données comme des octets bruts (raw bytes), et non comme des « chaînes de caractères ».

#### 4. `memcmp` vs `strcmp`

| Critère de comparaison | `memcmp` | `strcmp` |
| ------------------- | ------------------------------------------------------- | --------------------------------------------- |
| **Prototype de fonction** | `int memcmp(const void *s1, const void *s2, size_t n);` | `int strcmp(const char *s1, const char *s2);` |
| **Rôle** | Compare les `n` premiers **octets (bytes)** de deux blocs de mémoire | Compare deux **chaînes de caractères (strings)** |
| **Nécessite `n`** | **Oui**, `n` spécifie le nombre d'octets à comparer | **Non** |
| **Exige `\0`** | **Non** | **Oui, la chaîne doit se terminer par `\0`** |
| **Condition d'arrêt** | Après comparaison de `n` octets, ou dès le premier octet différent | Dès le premier caractère différent, ou à la rencontre de `\0` |
| **Cibles de comparaison** | Données mémoire arbitraires | Chaînes de caractères C |
| **Capacité à comparer des données binaires** | **Possible** | **Inadapté** |
| **Traite `\0` comme un terminateur spécial** | **Non**, `\0` est simplement un octet ordinaire | **Oui**, `\0` indique la fin de la chaîne |
| **Retourne `0`** | Les `n` premiers octets sont tous identiques | Le contenu des deux chaînes est identique |
| **Retourne `< 0`** | Dans le premier octet différent, `s1` est inférieur à `s2` | Dans le premier caractère différent, `s1` est inférieur à `s2` |
| **Retourne `> 0`** | Dans le premier octet différent, `s1` est supérieur à `s2` | Dans le premier caractère différent, `s1` est supérieur à `s2` |
| **Cas d'utilisation typiques** | Comparaison de tableaux, de mémoire brute dans des structures, de données binaires, etc. | Comparaison de noms d'utilisateur, de mots, de phrases et autres chaînes |
| **Exemple** | `memcmp(a, b, 10)` | `strcmp("abc", "abd")` |

`memcmp` compare un « nombre spécifié d'octets en mémoire », tandis que `strcmp` compare des « chaînes de caractères se terminant par `\0` ».