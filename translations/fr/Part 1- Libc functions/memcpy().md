`memcpy` : copie le contenu d'une zone mémoire vers une autre.

#### 1. Prototype

```c
#include <string.h>

void	*memcpy(void *dest, const void *src, size_t n);
```
Son rôle est de copier `n` octets à partir de la zone mémoire pointée par `src` vers la zone mémoire pointée par `dest`.
On peut le comprendre ainsi :
```txt
src  ──────────────► 读取
                      │
                      │ n 个 byte
                      ▼
dest ──────────────► 写入
```
Il retourne l'adresse de début de la zone mémoire cible. 

Notez que cette fonction n'est pas spécialement conçue pour copier des chaînes de caractères, elle ne se soucie pas de la nature des données. Il s'agit essentiellement d'une copie octet par octet (byte-by-byte) de mémoire brute, ce qui explique également pourquoi elle peut copier des structures : elle copie l'ensemble de la mémoire occupée par la structure. 

#### 2. Paramètres de la fonction

Lit `n` octets à partir de `src`, puis les écrit dans `dest`.

|Paramètre|Signification|
|---|---|
|`dest`|destination, adresse cible|
|`src`|source, adresse source|
|`n`|nombre d'octets à copier|
- dest : adresse de début de la zone mémoire cible
- src : adresse de début de la zone mémoire source, const void \*src indique que les données pointées par src ne peuvent pas être modifiées à l'intérieur de cette fonction

#### 3. Précautions

- memcpy n'ajoute pas automatiquement '\0'
- memcpy ne peut pas gérer les mémoires qui se chevauchent, c'est-à-dire qu'il ne peut pas traiter les situations où la zone source et la zone cible risquent de se superposer, c'est `undefined behavoir`, pour traiter des mémoires qui se chevauchent, il faut utiliser `memmove()`
- Lorsque n = 0, c'est-à-dire memcpy(dest, src, 0), 0 octet est copié, il n'y a donc pas de copie de données réelle, mais la fonction retourne tout de même dest
- dest et src doivent disposer d'un espace suffisant, ce qui constitue un problème de sécurité très important. 

[[strlcpy()]]