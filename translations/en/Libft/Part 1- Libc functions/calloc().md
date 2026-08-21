calloc (**c**ontiguous **alloc**ation) is a **dynamic memory allocation function** in the C standard library.
Its purpose is to allocate a block of **contiguous dynamic memory and initialize all bytes of this memory to `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

For example: allocating contiguous memory capable of holding **5 `int`**, and initializing all memory to `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

If `sizeof(int) == 4`, it allocates 5 x 4 = 20 bytes, and the memory can be visualized as:

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

The return value is `void *`, which returns the starting address of the allocated memory. If the allocation fails, it returns NULL. 

#### 2. Two Parameters of calloc

**calloc(number of elements, size of each element)**

1 `nmemb` (number of members): How many elements to allocate

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 means 10 ints are needed 

2 `size`: Represents how many bytes each element occupies

`calloc(10, sizeof(int))` is 10 x 4 = 40 bytes

3 `calloc` the parameters can lead to overflow issues

If `nmemb` and ''

#### 3. Differences Between calloc and malloc

`malloc(size_t size)`: Allocates memory of size bytes without initializing this memory

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

The contents of the memory obtained from malloc cannot be assumed to be 0; these values are indeterminate.

```c
int *array;

array = calloc(5, sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│  0 │  0 │  0 │  0 │  0 │
└────┴────┴────┴────┴────┘
```

calloc initializes every byte of the allocated memory to 0 

The memory sizes requested by malloc and calloc can be the same; the truly important difference is that malloc does not perform initialization, whereas calloc initializes all bytes of the memory to 0.