calloc (**c**ontiguous **alloc**ation) is a **dynamic memory allocation function** in the C standard library.
Its purpose is to request a block of contiguous dynamic memory and initialize all bytes of this memory to `0`.

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

For example: requesting contiguous memory capable of storing **5 `int`** and initializing all memory to `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

If `sizeof(int) == 4`, it is requesting `5 x 4 = 20 bytes`, and the memory can be visualized as:

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

#### 2. The 2 parameters of calloc

1 `nmemb` (number of members): How many elements to allocate

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 means 10 ints are needed 

2 `size`: Represents how many bytes each element occupies