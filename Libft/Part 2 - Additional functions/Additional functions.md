
### 阶段一：字符串的动态内存操作

#### 学习 malloc、字符串复制、指针偏移、二维指针和内存释放

- ft_substr
- ft_strjoin
- ft_strtrim
- ft_split

### 阶段二：数据类型转换

#### 学习整数位数计算、负数处理、INT_MIN 和字符转换

- ft_itoa

### 阶段三：函数指针

#### 学习函数指针、回调函数、索引和字符地址

- ft_strmapi
- ft_striteri

### 阶段四：文件描述符输出

#### 学习 write、文件描述符和整数输出

- ft_putchar_fd
- ft_putstr_fd
- ft_putendl_fd
- ft_putnbr_fd

#### 1.  ft_substr

```c
char *ft_substr(char const *s, unsigned int start, size_t len);
```

作用：从原始字符串 `s` 中的 `start` 位置开始，最多截取 `len` 个字符，并将截取的内容放进一个新的字符串中

| 部分                 | 含义           | 返回值                        |
| ------------------ | ------------ | -------------------------- |
| char *             | 返回一个字符指针     | 1. 内存申请成功，返回新字符串的首地址       |
| ft_substr          | 函数名称         | 2. malloc申请失败，返回NULL       |
| char const \*s     | 原始字符串，函数不修改它 | 3. 如果 start 已经超出原字符串的有效范围， |
| unsigned int start | 开始截取的位置      | 应该返回一个空字符串，而不是直接返回NULL     |
| size_t len         | 最多截取多少个字符    |                            |

这里有三个重要概念。

**a：为什么返回值是** `char *`**？**

因为函数通过 `malloc` 创建一个新的字符串，并返回这个字符串的首地址

**b：为什么** `s` **是** `char const *`**？**

因为这个函数只负责读取原字符串，不应该修改原字符串

**c：为什么** `len` **是** `size_t`**？**

因为它表示字符串长度或内存大小，是 C 语言中常用的无符号尺寸类型

#### 2. ft_strjoin

```c
char *ft_strjoin(char const *s1, char const *s2);
```

作用：将 s1 和 s2 两个字符串连接起来，创建一个新的字符串，并返回新字符串的首地址

注意：不是直接修改 s1，而是创建一个全新的字符串

#### 3.  ft_strtrim

```c
char *ft_strtrim(char const *s1, char const *set);
```

作用：表示从字符串的两端删除字符

注意：第2个参数 set 是一个字符集合, ft_strtrim 只删除字符串两端的指定字符，不删除字符串中间的指定字符, 是要求删除所有位于两端、且属于 set 这个字符集合的字符

#### 4.  ft_split

```c
char **ft_split(char const *s, char c);
```

作用：根据指定的分隔字符，将原始字符串分割成多个独立的字符串，并将这些字符串放进一个以 NULL 结尾的指针数组中

返回值：返回的是一个字符串数组，因此它的返回类型是二级指针  char **

例如：
```c
char **result;

result = ft_split("Hello 42 Libft", ' ');

```

最终逻辑上得到：
```c
result[0] = "Hello"
result[1] = "42"
result[2] = "Libft"
result[3] = NULL

```

注意：

- ft_split 不会修改原始字符串，而是通过 `malloc` 创建新的字符串

- 还有一个细节，连续出现的分隔字符会被忽略，不会产生空字符串

- 没有单词不代表函数返回 `NULL`.
  如果内存申请成功，函数应该返回一个只有 `NULL` 指针元素的数组

- 只要 malloc 成功，空字符串输入应该返回一个有效的指针数组，而不是 NULL

#### 5. ft_itoa

```c
char *ft_itoa(int n);
```

作用：把一个整数n转换成对应的字符串

返回值：

- 成功：返回一个新分配的字符串，表示整数 n
- 内存分配失败：返回 NULL

注意：返回的字符串由 `malloc` 分配，因此调用者使用完毕后必须 free

内存大小 = 数字位数 + 负号位置 + 字符串结束符

#### 6. ft_strmapi

```c
char *ft_strmapi(char const *s, char (*f)(unsigned int, char));
```

作用：使用函数 `f` 对字符串 s 中的每一个字符进行处理，并将处理后的字符放入一个新分配的字符串中

有两个重要要求：

- 原始字符串 s 不能被修改
- 返回一个新的字符串，必须通过 malloc 分配

注意：ft_strmapi 本身并不规定必须转换成大写。具体怎么转换，完全由调用者传入的函数 f 决定

ft_strmapi 并不知道如何处理字符，它只是负责遍历字符串，并把每个字符和索引交给调用者提供的函数 f，它创建一个新字符串，不修改原字符串

#### 7.  ft_striteri

```c
void ft_striteri(char *s, void (*f)(unsigned int, char *));
```

该函数直接修改原字符串，不创建新字符串，把当前字符的地址交给回调函数，由回调函数直接修改原字符串

注意：ft_striteri 不需要 malloc , 因为传递的是原字符串中字符的地址，回调函数直接修改原字符串中的字符，不需要创建新的字符串，因此：

- ft_striteri 内部不需要  malloc

- ft_striteri 内部不需要  free

- ft_striteri 不返回新字符串

- 调用者不需要因为调用 ft_striteri 而额外释放内存

这也是它和 ft_strmapi 在内存管理方面的一个重要区别

#### 8.  ft_putchar_fd

```c
void ft_putchar_fd(char c, int fd);
```

作用：将一个字符写入指定的文件描述符（file descriptor，缩写成fd)

注意：传入的是字符，而不是字符串

函数的第1个参数是需要输出的字符，第2个参数是文件描述符 fd, 文件描述符是操作系统用来标识打开文件或输入输出资源的整数

在 Unix/Linux/macOS 系统中，最常见的三个文件描述符是：

| 文件描述符 | 名称              | 用途         |
| ----- | --------------- | ---------- |
| 0     | `STDIN_FILENO`  | 标准输入，通常是键盘 |
| 1     | `STDOUT_FILENO` | 标准输出，通常是终端 |
| 2     | `STDERR_FILENO` | 标准错误，通常是终端 |

ft_putchar_fd 不需要使用 malloc() 或  free()

原因是：

- c 是函数的局部参数变量

- &c 是这个变量的地址

- write() 直接从这个地址读取一个字节

- 不需要创建动态分配的内存

#### 9.  ft_putstr_fd

```c
void ft_putstr_fd(char *s, int fd);
```

ft_putstr_fd 的作用与  ft_putchar_fd 类似，但它写入的是**整个字符串**.

它有两个参数：

- s：需要写入的字符串

- fd：指定写入目标的文件描述符

返回类型是 `void`，表示函数不返回任何值

**如果字符串长度不是固定的，我们如何知道应该写入多少个字节？**

显然，我们不能每次手动计算字符串长度, 这时就需要使用之前学过的 ft_strlen()

**ft_strlen() 在 ft_putstr_fd 中的作用**

它返回字符串中有效字符的数量，不包括最后的 '\0'

**ft_putstr_fd() 不需要 malloc()，也不需要 free() 

原因：

- `s` 是调用者提供的字符串地址

- `ft_strlen()` 只负责计算字符串长度

- `write()` 直接从字符串所在的内存读取数据

- 函数没有创建新的动态内存

因此 ft_putstr_fd() 不拥有字符串 s 的内存，也不应该释放它

#### 10.  ft_putendl_fd

```c
void ft_putendl_fd(char *s, int fd);
```

ft_putendl_fd 和 ft_putstr_fd  非常相似，唯一最重要的区别是：

ft_putendl_fd 在输出字符串之后，会自动追加一个换行符 '\n', 每次调用 ft_putendl_fd，都会在字符串后面自动添加一个换行符

两个参数：

- s：需要输出的字符串

- fd：指定写入目标的文件描述符

返回类型是 `void`，不返回任何值

ft_putendl_fd 不需要 malloc()或 free()

原因：

- s 是调用者提供的字符串

- ft_putstr_fd 直接读取字符串并写入目标

- ft_putchar_fd 直接写入一个换行符

- 整个过程没有创建动态分配的内存

因此，ft_putendl_fd 不负责释放字符串 s

**函数对比：

|函数|功能|是否自动换行|
|---|---|---|
|`ft_putchar_fd`|输出一个字符|否|
|`ft_putstr_fd`|输出一个字符串|否|
|`ft_putendl_fd`|输出一个字符串|是|

它们的底层实现都使用了 write()，另外，这三个函数都不需要动态内存分配

#### 11.   ft_putnbr_fd

```c
void ft_putnbr_fd(int n, int fd);
```

作用是将一个整数转换成十进制字符，并写入指定的文件描述符

这个函数比前面三个稍微复杂，因为需要处理：

- 正整数

- 负整数

- 数字 `0`

- INT_MIN（int 类型能够表示的最小负数）

这个函数和 ft_putchar_fd、ft_putstr_fd、ft_putendl_fd 一样，都是将数据写入指定的文件描述符

但它有一个不同之处：ft_putnbr_fd 接收的是整数 int ，需要将整数转换成十进制字符，然后输出

两个参数：
- n：需要输出的整数

- fd：指定写入目标的文件描述符

返回类型是 void，表示不返回任何值