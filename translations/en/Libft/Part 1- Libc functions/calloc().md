calloc (**c**ontiguous **alloc**ation) is a **dynamic memory allocation function** in the C standard library.
Its purpose is to request a block of **contiguous dynamic memory and initialize all bytes of this memory to `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

For example: requesting contiguous memory capable of storing **5 `int`**, and initializing all memory to `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

If `sizeof(int) == 4`, it requests 5 x 4 = 20 bytes, and the memory can be visualized as:

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

The return value is `void *`, which is the starting address of the allocated memory. If allocation fails, it returns NULL. 

#### 2. Two parameters of calloc

**calloc(number of elements, size of each element)**

1 `nmemb` (number of members) : How many elements to allocate

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 means 10 ints are needed 

2  `size` : Represents how many bytes each element occupies

`calloc(10, sizeof(int))` means 10 x 4 = 40 bytes

3 The `calloc` parameter can lead to overflow issues

If both `nmemb` and `size` are very large, the value of `nmemb x size` might exceed the maximum value that `size_t` can represent. This is an integer overflow, which may cause the actual allocated memory to be smaller than the caller expects.

4 `calloc(0, sizeof(int))` is a special case

Requesting 0 x sizeof(int) = 0 bytes. The C standard allows this call to succeed and return a pointer, or it may return NULL. If NULL is returned, this pointer cannot be used to access an object. Therefore, when implementing `ft_calloc`, `nmemb == 0` cannot simply be treated as a normal failure case. 

5 After using `calloc`, you must free it. Forgetting to `free()` may result in a memory leak. 

#### 3. Differences between calloc and malloc

`malloc(size_t size)` : Allocates size bytes of memory without initializing this memory

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

The amount of memory requested by malloc and calloc can be the same. The truly important difference is that malloc does not perform initialization, whereas calloc initializes all bytes of the memory to 0.

#### 4. Implementing ft_calloc

Core logic:

1 Calculate how many bytes are needed
2 Prevent `nmemb * size` overflow
3 Initialize all allocated memory to 0 

                ft_calloc
                    │
                    ▼
          Calculate nmemb × size
                    │
            Did overflow occur?
              /          \
            Yes           No
            ↓              ↓
         return NULL    malloc(total)
                           │
                   Allocation successful?
                       /       \
                     No         Yes
                     ↓           ↓
                  return NULL   Zero out
                                  │
                                  ↓
                               return ptr

**`calloc(nmemb, size)` requests contiguous dynamic memory for `nmemb` elements of `size` bytes each, and initializes all bytes of this memory to `0`**