calloc (**c**ontiguous **alloc**ation) is a **dynamic memory allocation function** in the C standard library.
Its purpose is to allocate a block of **contiguous dynamic memory, and initialize all bytes of this memory to `0`.** 

#### 1. Prototype

```c
void *calloc(size_t nmemb, size_t size);
```

For example: allocating contiguous memory capable of holding **5 `int`**, and initializing all memory to `0`

```c
int *array;

array = calloc(5, sizeof(int));

```

If `sizeof(int) == 4`, it means requesting 5 x 4 = 20 bytes, and the memory can be understood as: 

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

The return value is `void *`, which means returning the starting address of the allocated memory. If allocation fails, NULL is returned. 

#### 2. The 2 parameters of calloc

**calloc(number of elements, size of each element)**

1 `nmemb` (number of members): how many elements to allocate

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 means 10 int are needed 

2  `size` : indicates how many bytes an element takes up

`calloc(10, sizeof(int))` means 10 x 4 = 40 bytes

3 `calloc` parameters can cause overflow issues

If `nmemb` and `size` are both very large, then `nmemb x size`'s value may exceed `size_t` can represent. This is integer overflow, which may cause the actual allocated memory to be smaller than the caller expects.

4 `calloc(0, sizeof(int))` is a special case

Requesting 0 x sizeof(int) = 0 bytes, the C standard allows such a call to succeed and return a pointer, and also allows returning NULL. If it returns NULL, this pointer cannot be used to access an object, so when implementing `ft_calloc`, `nmemb == 0` Cannot simply be treated as a normal failure case. 

5 After using `calloc`, it must be freed; if you forget `free()` it may cause a memory leak. 

#### 3. Difference between calloc and malloc

`malloc(size_t size)` :  Allocates size bytes of memory, without initializing this memory

```c
int *array = malloc(5 * sizeof(int));

array
  ↓
┌────┬────┬────┬────┬────┐
│ ?? │ ?? │ ?? │ ?? │ ?? │
└────┴────┴────┴────┴────┘
```

The contents of the memory obtained by malloc cannot be assumed to be 0; these values are indeterminate.

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

The memory size requested by malloc and calloc can be the same; the real key difference is that malloc does not perform initialization, whereas calloc initializes all bytes of the memory to 0.

#### 4. Implementing ft_calloc

Core logic:

1 Calculate how many bytes are required
2 Prevent `nmemb * size` overflow
3 Initialize all allocated memory to 0 

                ft_calloc
                    │
                    ▼
          Calculate nmemb × size
                    │
            Does overflow occur?
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


**`calloc(nmemb, size)` Allocate `nmemb` items, each of `size` bytes of contiguous dynamic memory, and initialize all bytes of this memory to `0`**

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
