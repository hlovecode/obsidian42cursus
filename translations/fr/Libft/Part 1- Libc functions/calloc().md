calloc (**c**ontiguous **alloc**ation) est une **fonction d'allocation dynamique de mémoire** de la bibliothèque standard C.
Son rôle est de demander un bloc de **mémoire dynamique continue, et d'initialiser tous les octets de cette mémoire à `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

Par exemple : demander de la mémoire continue pouvant contenir **5 `int`**, et initialiser toute la mémoire à `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

Si `sizeof(int) == 4`, c'est demander 5 x 4 = 20 octets, la mémoire peut être représentée comme :

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

La valeur de retour est `void *`, c'est-à-dire qu'elle renvoie l'adresse de début de la mémoire allouée ; si l'allocation échoue, elle renvoie NULL. 

#### 2. Les 2 paramètres de calloc

**calloc(nombre d'éléments, taille de chaque élément)**

1 `nmemb` (number of members) : combien d'éléments à allouer

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 signifie qu'il faut 10 int 

2  `size` : indique combien d'octets chaque élément occupe

`calloc(10, sizeof(int))` c'est 10 x 4 = 40 octets

3 `calloc` les paramètres peuvent entraîner un problème de dépassement

Si `nmemb` et `size` sont tous deux très grands, alors `nmemb x size` peut dépasser `size_t` la valeur maximale que peut représenter , c'est un dépassement d'entier, ce qui peut conduire à ce que la mémoire réellement allouée soit plus petite que ce que l'appelant pense.

4 `calloc(0, sizeof(int))` est un cas particulier

Demander 0 x sizeof(int) = 0 octet, la norme C autorise cet appel à réussir et à renvoyer un pointeur, ou à renvoyer NULL ; s'il renvoie NULL, ce pointeur ne peut pas être utilisé pour accéder à un objet, c'est pourquoi lors de l'implémentation de `ft_calloc` , `nmemb == 0` Ne peut pas être simplement traité comme un échec ordinaire. 

5 Après l'utilisation de `calloc`, il faut utiliser free, si vous oubliez `free()` cela peut provoquer une fuite de mémoire. 

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

Le contenu de la mémoire obtenue par malloc ne peut pas être supposé être 0, ces valeurs sont indéterminées.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc va initialiser chaque octet de la mémoire allouée à 0 

La taille de la mémoire demandée par malloc et calloc peut être identique, la vraie différence importante est que malloc ne fait aucune initialisation, tandis que calloc initialise tous les octets de la mémoire à 0.

#### 4. Implémentation de ft_calloc

Logique principale :

1 Calculer le nombre d'octets nécessaires
2 Éviter `nmemb * size` un débordement
3 Initialiser toute la mémoire allouée à 0 

                ft_calloc
                    │
                    ▼
          Calculer nmemb × size
                    │
            Y a-t-il un débordement ?
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


**`calloc(nmemb, size)` Allouer `nmemb` éléments, chacun de `size` octets de mémoire dynamique contiguë, et initialiser tous les octets de cette mémoire à `0`**

---

## 中文原文

calloc (**c**ontiguous **alloc**ation) 是 C 标准库中的**动态内存分配函数**.
它的作用是申请一块**连续的动态内存，并且把这块内存的所有字节初始化为 `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

例如：申请能够存放 **5 个 `int`** 的连续内存，并且把所有内存初始化为 `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

如果 `sizeof(int) == 4`, 就是申请  5 x 4 = 20 bytes , 内存可理解成：

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

返回值是 `void *`, 也就是返回所分配内存的起始地址，如果分配失败，则返回 NULL. 

#### 2. calloc 的2个参数

**calloc(元素数量，每个元素大小)**

1 `nmemb` (number of members) ：要分配多少个元素

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 表示需要 10 个 int 

2  `size` : 表示元素占多少字节

`calloc(10, sizeof(int))` 就是 10 x 4 = 40 bytes

3 `calloc` 参数会带来溢出问题

如果 `nmemb` 和 `size` 都非常大，那 `nmemb x size` 的值可能超过 `size_t` 能表示的最大值，这是整数溢出, 可能导致实际申请的内存比调用者以为的小.

4 `calloc(0, sizeof(int))` 是一个特殊情况

请求 0 x sizeof(int) = 0 bytes, C 标准允许这种调用成功且返回一个指针，也允许返回 NULL,  如果返回 NULL, 这个指针不能用于访问对象, 因此实现 `ft_calloc` 时，`nmemb == 0` 不能简单地当成普通失败情况. 

5 使用完 `calloc` 后必须 free, 如果忘记 `free()` 可能会产生内存泄漏. 

#### 3. calloc 和 malloc 的区别

`malloc(size_t size)` :  分配 size 个字节的内存，不会初始化这块内存

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

malloc 得到的内存内容不能假定是 0, 这些值是不确定的.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc 会把分配出来的内存的每一个字节初始化为 0 

malloc 和 calloc 申请的内存大小可以相同，真正的重要区别是malloc不会做初始化，calloc会对内存的所有字节初始化为 0.

#### 4. 实现 ft_calloc

核心逻辑：

1 计算需要多少字节
2 防止 `nmemb * size` 溢出
3 把分配的内存全部初始化为0 

                ft_calloc
                    │
                    ▼
          计算 nmemb × size
                    │
            是否发生溢出？
              /          \
            是            否
            ↓              ↓
         return NULL    malloc(total)
                           │
                      分配成功？
                       /       \
                     否         是
                     ↓           ↓
                  return NULL   清零
                                  │
                                  ↓
                               return ptr


**`calloc(nmemb, size)` 申请 `nmemb` 个、每个 `size` 字节的连续动态内存，并将这块内存的所有字节初始化为 `0`**
