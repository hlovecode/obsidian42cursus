`strnstr` sert à chercher la première occurrence de la chaîne `needle` dans les premiers len caractères de la chaîne `haystack`.

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

Paramètres :

- haystack : la chaîne dans laquelle effectuer la recherche
- needle : la chaîne à rechercher, c'est-à-dire la sous-chaîne
- len : le nombre maximal de caractères de haystack à parcourir, contrôle la limite de recherche dans haystack

Valeur de retour :

Un pointeur vers la première occurrence de needle dans haystack, ou NULL si la sous-chaîne n'est pas trouvée, ou haystack si needle est une chaîne vide.

#### 2. Logique centrale de `strnstr`

1. needle est-elle une chaîne vide ? Si oui, retourner haystack
2. Chercher les points de départ possibles dans les len premiers caractères de haystack
3. Pour chaque point de départ possible : vérifier si needle correspond entièrement
4. La correspondance est-elle réussie ? Si oui, retourner la position actuelle
5. A-t-on tout vérifié ? Si oui, retourner NULL

`strnstr` : Recherche la première occurrence complète de `needle` dans les `len` premiers caractères de `haystack` ; renvoie un pointeur si elle est trouvée, `NULL` si elle ne l'est pas, et `needle` si `haystack` est une chaîne vide.

#### 3. Comparaison avec des fonctions similaires

| Fonction | Objet de la recherche | Limite de la zone de recherche |
| --------- | ---------- | -------- |
| `strstr` | Sous-chaîne dans une chaîne | Non limitative |
| `strnstr` | Sous-chaîne dans une chaîne | Limitative |
| `strchr` | Caractère unique | Non limitative |
| `strrchr` | Dernière occurrence d'un caractère unique | Non limitative |
| `strncmp` | Comparaison de deux chaînes | Limitative |

- `strchr` : Recherche un caractère
- `strstr` : Recherche une chaîne
- `strnstr` : Recherche une chaîne sur une longueur limitée
- `strncmp` : Compare les n premiers caractères de deux chaînes