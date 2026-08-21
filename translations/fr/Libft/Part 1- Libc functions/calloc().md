calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard C.
Son rôle est d'allouer un bloc de **mémoire dynamique contiguë et d'initialiser tous les octets de cette mémoire à `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

Par exemple : allouer de la mémoire contiguë pouvant stocker **5 `int`** et initialiser toute la mémoire à `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

Si `sizeof(int) == 4`, cela alloue 5 x 4 = 20 octets, et la mémoire peut être visualisée comme suit :

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

La valeur de retour est `void *`, c'est-à-dire l'adresse de début de la mémoire allouée ; si l'allocation échoue, elle retourne NULL. 

#### 2. Les 2 paramètres de calloc

**calloc(nombre d'éléments, taille de chaque élément)**

1 `nmemb` (number of members) : le nombre d'éléments à allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie que 10 int sont nécessaires 

2  `size` : indique le nombre d'octets par élément

`calloc(10, sizeof(int))` représente 10 x 4 = 40 octets

3 Le paramètre `calloc` peut entraîner des problèmes de dépassement (overflow)

Si `nmemb` et `size` sont tous deux très grands, la valeur de `nmemb x size` peut dépasser la valeur maximale représentable par `size_t`, ce qui constitue un dépassement d'entier et peut amener la mémoire réellement allouée à être plus petite que ce que l'appelant imagine.

4 `calloc(0, sizeof(int))` est un cas particulier

Demander 0 x sizeof(int) = 0 octet. La norme C autorise cet appel à réussir et à retourner un pointeur, ou à retourner NULL. Si NULL est retourné, ce pointeur ne peut pas être utilisé pour accéder à un objet. Par conséquent, lors de l'implémentation de `ft_calloc`, `nmemb == 0` ne peut pas être simplement traité comme un échec ordinaire. 

5 Après avoir utilisé `calloc`, il est obligatoire d'appeler free ; oublier de `free()` peut provoquer une fuite de mémoire. 

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

Le contenu de la mémoire obtenue via malloc ne peut pas être supposé égal à 0, ces valeurs sont indéterminées.

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

La taille de la mémoire allouée par malloc et calloc peut être identique, la véritable différence importante est que malloc n'effectue pas d'initialisation, tandis que calloc initialise tous les octets de la mémoire à 0.

#### 4. Implémentation de ft_calloc

Logique principale :

1 Calculer le nombre d'octets nécessaires
2 Prévenir le dépassement (overflow) de `nmemb * size`
3 Initialiser toute la mémoire allouée à 0 

                ft_calloc
                    │
                    ▼
          Calculer nmemb × size
                    │
            Y a-t-il dépassement ?
              /          \
            Oui           Non
            ↓              ↓
         return NULL    malloc(total)
                           │
                      Allocation réussie ?
                       /       \
                     Non        Oui
                     ↓           ↓
                  return NULL   Mise à zéro
                                  │
                                  ↓
                               return ptr

**`calloc(nmemb, size)` alloue de la mémoire dynamique contiguë pour `nmemb` éléments de `size` octets chacun, et initialise tous les octets de cette mémoire à `0`**