calloc (**c**ontiguous **alloc**ation) 是 C 标准库中的**动态内存分配函数**.
它的作用是申请一块连续的动态内存，并且把这块内存的所有字节初始化为 `0`.

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

#### 2. calloc 的2个参数

**calloc(元素数量，每个元素大小)**

1 `nmemb` (number of members) ：要分配多少个元素

```c
calloc(10, sizeof(int));
```

`nmemb` = 10 表示需要 10 个 int 

2  `size` : 表示元素占多少字节

`calloc(10, sizeof(int))` 就是 10 x 4 = 40 bytes

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

calloc 会把分配出来的内存的每一个字节