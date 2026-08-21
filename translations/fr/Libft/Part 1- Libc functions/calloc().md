calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard du C.
Son rôle est d'allouer un bloc de mémoire dynamique contiguë et d'initialiser tous les octets de cette mémoire à `0`.

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

Par exemple : allouer de la mémoire contiguë pouvant stocker **5 `int`**, et initialiser toute la mémoire à `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

Si `sizeof(int) == 4`, c'est-à-dire une allocation de `5 x 4 = 20 bytes`, la mémoire peut être représentée comme :

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

1 `nmemb` (nombre d'éléments) : le nombre d'éléments à allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie que l'on a besoin de 10 int 

2  `size` : indique le nombre d'octets par élément