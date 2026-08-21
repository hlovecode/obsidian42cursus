calloc (**c**ontiguous **alloc**ation) is a **dynamic memory allocation function** in the C standard library.
Its purpose is to allocate a contiguous block of dynamic memory and initialize all bytes of this memory to `0`.

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

For example: allocate contiguous memory capable of holding **5 `int`**, and initialize all memory to `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

If `sizeof(int) == 4`, it allocates 5 x 4 = 20 bytes, and the memory can be conceptualized as:

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

#### 2. Two parameters of calloc

**calloc(number of elements, size of each element)**

1 `nmemb` (number of members): how many elements to allocate

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 means 10 ints are needed

2 `size`: represents how many bytes each element occupies

`calloc(10, sizeof(int))` is 10 x 4 = 40 bytes

#### 3. Differences between calloc and malloc

`malloc(size_t size)`: allocates memory of `size` bytes and does not initialize this memory

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

The content of memory obtained via malloc cannot be assumed to be 0; these values are indeterminate.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc initializes every byte of the allocated memory