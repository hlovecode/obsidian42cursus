
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

- 

#### 1.  ft_substr

```c
char *ft_substr(char const *s, unsigned int start, size_t len);
```

#### 2. ft_strjoin

```c
char *ft_strjoin(char const *s1, char const *s2);
```

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
