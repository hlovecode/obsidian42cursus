calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard C.
Son rôle est de demander un bloc de mémoire dynamique contiguë et d'initialiser tous les octets de cette mémoire à `0`.

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

Par exemple : demander une mémoire contiguë pouvant stocker **5 `int`** et initialiser toute la mémoire à `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

Si `sizeof(int) == 4`, cela demande 5 x 4 = 20 octets, et la mémoire peut être représentée ainsi :

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

#### 2. Les 2 paramètres de calloc

**calloc(nombre d'éléments, taille de chaque élément)**

1 `nmemb` (nombre d'éléments) : combien d'éléments il faut allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie que l'on a besoin de 10 int

2 `size` : représente le nombre d'octets par élément

`calloc(10, sizeof(int))` fait 10 x 4 = 40 octets

#### 3. Différence entre calloc et malloc

`malloc(size_t size)` : alloue size octets de mémoire, n'initialise pas cette mémoire

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

Le contenu de la mémoire obtenue ne peut pas être supposé égal à 0, ces valeurs sont indéterminées.

`calloc`