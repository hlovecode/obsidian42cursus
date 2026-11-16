
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

**1：为什么返回值是** `char *`**？**

因为函数通过 `malloc` 创建一个新的字符串，并返回这个字符串的首地址

**2：为什么** `s` **是** `char const *`**？**

因为这个函数只负责读取原字符串，不应该修改原字符串

**3：为什么** `len` **是** `size_t`**？**

因为它表示字符串长度或内存大小，是 C 语言中常用的无符号尺寸类型

#### 2. ft_strjoin

```c
char *ft_strjoin(char const *s1, char const *s2);
```

作用：将 s1 和 s2 两个字符串连接起来，创建一个新的字符串，并返回新字符串的首地址

注意：不是直接修改 `s1`，而是创建一个全新的字符串

#### 3.  ft_strtrim

```c
char *ft_strtrim(char const *s1, char const *set);
```

#### 4.  ft_split

```c
char **ft_split(char const *s, char c);
```

#### 5. ft_itoa

```c
char *ft_itoa(int n);
```

#### 6. ft_strmapi

```c
char *ft_strmapi(char const *s, char (*f)(unsigned int, char));
```

#### 7.  ft_striteri

```c
void ft_striteri(char *s, void (*f)(unsigned int, char *));
```

#### 8.  ft_putchar_fd

```c
void ft_putchar_fd(char c, int fd);
```

#### 9.  ft_putstr_fd

```c
void ft_putstr_fd(char *s, int fd);
```

#### 10.  ft_putendl_fd

```c
void ft_putendl_fd(char *s, int fd);
```

#### 11.   ft_putnbr_fd

```c
void ft_putnbr_fd(int n, int fd);
```
