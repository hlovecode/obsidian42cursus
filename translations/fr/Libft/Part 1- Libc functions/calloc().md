calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard du C.
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

Si `sizeof(int) == 4`, cela demande 5 x 4 = 20 octets, et la mémoire peut être visualisée comme suit :

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

La valeur de retour est un `void *`, c'est-à-dire qu'elle renvoie l'adresse de début de la mémoire allouée. Si l'allocation échoue, elle renvoie NULL. 

#### 2. Les 2 paramètres de calloc

**calloc(nombre d'éléments, taille de chaque élément)**

1 `nmemb` (number of members) : le nombre d'éléments à allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie que l'on a besoin de 10 int 

2 `size` : représente le nombre d'octets par élément

`calloc(10, sizeof(int))` est donc 10 x 4 = 40 octets

3 `calloc` Les paramètres peuvent poser un problème de dépassement (overflow)

Si `nmemb` et ''

#### 3. Différence entre calloc et malloc

`malloc(size_t size)` : Alloue une mémoire de size octets, sans initialiser cette mémoire

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

Le contenu de la mémoire obtenue avec malloc ne peut pas être supposé égal à 0, ces valeurs sont indéterminées.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc initialise chaque octet de la mémoire allouée à 0 

La taille de la mémoire demandée par malloc et calloc peut être la même, mais la véritable différence importante est que malloc n'effectue pas d'initialisation, tandis que calloc initialise tous les octets de la mémoire à 0.