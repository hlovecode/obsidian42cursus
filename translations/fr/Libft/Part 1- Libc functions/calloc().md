calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard C.
Son rôle est de demander un bloc de **mémoire dynamique contiguë et d'initialiser tous les octets de cette mémoire à `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

Par exemple : demander une mémoire contiguë pouvant stocker **5 `int`** et initialiser toute la mémoire à `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

Si `sizeof(int) == 4`, il s'agit de demander 5 x 4 = 20 octets, la mémoire peut être représentée ainsi :

```c
array
  ↓
┌────┬────┬────┬────┬────┐
│  0  │  0  │  0  │  0  │  0  │
└────┴────┴────┴────┴────┴────┘
 int   int   int   int   int
 
array[0] == 0
array[1] == 0
array[2] == 0
array[3] == 0
array[4] == 0
```

La valeur de retour est un `void *`, c'est-à-dire l'adresse de début de la mémoire allouée. Si l'allocation échoue, elle retourne NULL. 

#### 2. Les 2 paramètres de calloc

**calloc(nombre d'éléments, taille de chaque élément)**

1 `nmemb` (number of members) : le nombre d'éléments à allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie que l'on a besoin de 10 int 

2 `size` : représente le nombre d'octets par élément

`calloc(10, sizeof(int))` représente 10 x 4 = 40 octets

3 Les paramètres de `calloc` peuvent entraîner des problèmes de dépassement (overflow)

Si `nmemb` et `size` sont tous les deux très grands, la valeur de `nmemb x size` peut dépasser la valeur maximale que `size_t` peut représenter. C'est un dépassement d'entier (integer overflow), ce qui peut faire en sorte que la mémoire réellement allouée soit plus petite que ce que l'appelant pensait.

4 `calloc(0, sizeof(int))` est un cas particulier

Demander 0 x sizeof(int) = 0 octet. La norme C autorise cet appel à réussir et à retourner un pointeur, ou à retourner NULL. Si NULL est retourné, ce pointeur ne peut pas être utilisé pour accéder à un objet. Par conséquent, lors de l'implémentation de `ft_calloc`, `nmemb == 0` ne peut pas être traité simplement comme un cas d'échec ordinaire. 

5 Après avoir utilisé `calloc`, il est obligatoire d'appeler free. Si l'on oublie de `free()`, cela peut provoquer une fuite de mémoire (memory leak). 

#### 3. Différence entre calloc et malloc

`malloc(size_t size)` : alloue size octets de mémoire, sans initialiser cette mémoire.

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

Le contenu de la mémoire obtenue par malloc ne peut pas être supposé égal à 0, ces valeurs sont indéterminées.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc initialise chaque octet de la mémoire allouée à 0.

La taille de la mémoire demandée par malloc et calloc peut être identique. La véritable différence importante est que malloc ne fait pas d'initialisation, tandis que calloc initialise tous les octets de la mémoire à 0.

#### 4. Implémentation de ft_calloc

Logique principale :

1 Calculer le nombre d'octets nécessaires
2 Prévenir 

                ft_calloc
                    │
                    ▼
          Calculer nmemb × size
                    │
            Y a-t-il un dépassement ?
              /          \
            Oui           Non
            ↓              ↓
         return NULL    malloc(total)
                           │
                    Allocation réussie ?
                       /       \
                     Non        Oui
                     ↓           ↓
                  return NULL   Mettre à zéro
                                  │
                                  ↓
                               return ptr