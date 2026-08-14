`strnstr` est utilisé pour rechercher la première occurrence de la chaîne `needle` dans les premiers len caractères de la chaîne `haystack`.

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

Paramètres :

- haystack : la chaîne dans laquelle effectuer la recherche
- needle : la chaîne à rechercher, c'est-à-dire la sous-chaîne
- len : nombre maximal de caractères de haystack à parcourir ; cela contrôle la limite de la recherche dans haystack

Valeur de retour :

Un pointeur vers la première occurrence de needle dans haystack, ou NULL si needle n'est pas trouvé. Si needle est une chaîne vide, retourne haystack.

#### 2. Logique principale de `strnstr`

1. Est-ce que needle est une chaîne vide ? Si oui, retourne haystack.
2. Rechercher les points de départ possibles dans les premiers len caractères de haystack.
3. Pour chaque point de départ possible : vérifier si needle correspond entièrement.
4. La correspondance a-t-elle réussi ? Si oui, retourner la position actuelle.
5. Tout a-t-il été vérifié ? Si oui, retourner NULL.

`strnstr` : Recherche la première occurrence complète de `needle` dans les `len` premiers caractères de `haystack` ; retourne un pointeur en cas de succès, `NULL` en cas d'échec, ou `haystack` si `needle` est une chaîne vide.

#### 3. Comparaison avec des fonctions similaires

| Fonction    | Objet de la recherche | Limite la plage de recherche |
| --------- | ---------- | -------- |
| `strstr`  | Sous-chaîne dans une chaîne | Non |
| `strnstr` | Sous-chaîne dans une chaîne | Oui |
| `strchr`  | Caractère unique | Non |
| `strrchr` | Dernière occurrence d'un caractère unique | Non |
| `strncmp` | Comparaison de deux chaînes | Oui |

- `strchr` : Trouve un caractère
- `strstr`