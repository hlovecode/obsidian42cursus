`strncmp` compare au maximum les `n` premiers caractères.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Il sert à comparer octet par octet `s1` et `s2` depuis le début, sur un maximum de `n` caractères ; il s'arrête dès le premier caractère différent ou `\0`. Si tous les caractères comparés sont identiques, il renvoie `0`, sinon il renvoie une valeur négative ou positive selon la relation de grandeur du premier caractère différent.

Valeur de retour :

| Résultat de la comparaison | Valeur de retour |
|---|---|
| Les `n` premiers caractères de `s1` sont identiques à `s2` | `0` |
| `s1` est inférieur à `s2` | `< 0` |
| `s1` est supérieur à `s2` | `> 0` |

Remarque : Ne dépendez pas de la valeur exacte -1 ou 1, la norme garantit seulement < 0, = 0 ou > 0.

#### 2. Différence entre `strncmp` et `strcmp`

`strcmp` compare la chaîne entière, tandis que `strncmp` compare au maximum les n premiers caractères.

| | strcmp | strncmp |
| -------- | -------- | --------- |
| En-tête | string.h | string.h |
| Compare des chaînes | oui | oui |
| Nombre de paramètres | 2 | 3 |
| Limite la longueur de comparaison | non | oui |
| Nombre max. de caractères comparés | Illimité | n caractères |
| Renvoie 0 | Égales | Les n premiers caractères sont égaux |

#### 3. Application de `strncmp`

Cette fonction est idéale pour déterminer le préfixe d'une chaîne de caractères.

Exemple : Déterminer si « quit_now » commence par « quit »

```c
if (strncmp(command, "quit", 4) == 0)
{
	...
}
```

Les 3 points les plus cruciaux pour `strncmp` :

- n est le « nombre maximal de caractères à comparer », il n'est pas obligatoire de comparer n caractères.
- S'arrête dès le 1er caractère différent.
- La valeur de retour dépend uniquement du signe, ne vous fiez pas au chiffre exact :

```c
if (strncmp(s1, s2, n) < 0)

if (strncmp(s1, s2, n) == 0)

if (strncmp(s1, s2, n) > 0)
```

Ne pas écrire :

```c
if (strncmp(s1, s2, n) == -1)
```

Car la norme ne garantit pas de renvoyer systématiquement -1.

L'essence de `n` / `strncmp` est :

- Dans une fenêtre de taille maximale `n`, trouver le premier caractère différent entre `s1` et `s2`.
- S'il est trouvé, on le compare ; s'il n'est pas trouvé, on renvoie 0.