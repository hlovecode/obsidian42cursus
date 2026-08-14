`strnstr` est utilisé pour rechercher la première occurrence de la chaîne `needle` dans les `haystack` premiers caractères de la chaîne `haystack`.

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

Paramètres :

- haystack : la chaîne dans laquelle effectuer la recherche
- needle : la chaîne à rechercher, c'est-à-dire la sous-chaîne
- len : nombre maximal de caractères de haystack à parcourir pour la recherche, contrôlant ainsi la limite de recherche dans haystack

Valeur de retour :

Un pointeur vers la première occurrence de needle dans haystack. Si la chaîne n'est pas trouvée, retourne NULL. Si needle est une chaîne vide, retourne 

#### 2. Comparaison avec des fonctions similaires

| Fonction  | Objet de recherche | Limite de recherche |
| --------- | ------------------ | ------------------- |
| `strstr`  | Sous-chaîne dans une chaîne | Non |
| `strnstr` | Sous-chaîne dans une chaîne | Oui |
| `strchr`  | Caractère unique | Non |
| `strrchr` | Dernière occurrence d'un caractère unique | Non |
| `strncmp` | Comparaison de deux chaînes | Oui |