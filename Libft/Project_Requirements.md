使用C语言实现一些函数，比如重新实现libc，通过创建makefile，执行make命令，生成一个静态公共库libft.a.
<font color="red">这是整个Common Core的基础库.</font>
###### 第1组 字符判断：
```c
ft_isalpha

ft_isdigit

ft_isalnum

ft_isascii

ft_isprint
```
###### 第2组 内存操作
```c
memset

bzero

memcpy

memmove

memcmp

memchr
```
###### 第3组 字符串函数
```c
strlen

strlcpy

strlcat

strchr

strrchr

strncmp

strnstr

strdup
```
###### 第4组 字符转换
```c
toupper

tolower
```
###### 第5组 数字转换
```c
atoi
```
###### 第6组 动态内存
```c
calloc // 不同系统，行为可能不同
strdup
```
###### 第7组 要求自己写的新函数
```c
ft_substr
ft_strjoin
ft_strtrim
ft_split
ft_itoa
ft_strmapi
ft_striteri
ft_putchar_fd
ft_putstr_fd
ft_putendl_fd
ft_putnbr_fd
```
###### 第8组 Linked List 链表函数
| 函数                | 功能                   |
| ----------------- | -------------------- |
| `ft_lstnew`       | 创建新节点                |
| `ft_lstadd_front` | 头插                   |
| `ft_lstsize`      | 统计节点数量               |
| `ft_lstlast`      | 获取最后一个节点             |
| `ft_lstadd_back`  | 尾插                   |
| `ft_lstdelone`    | 删除一个节点               |
| `ft_lstclear`     | 删除整个链表               |
| `ft_lstiter`      | 遍历链表，对每个节点执行函数       |
| `ft_lstmap`       | 对每个节点内容进行转换，生成一个新的链表 |

### 1. Technical considerations 技术要求

1. **禁止使用全局变量**
因为Libft是一个公共库，应该同样输入 -> 永远同样输出.
如果有全局变量，当修改了该变量，会引发最终的结果发生变化.

2. **Helper Function 必须static**
例如: 
```c
ft_split()
```
里面需要
```c
int count_words()
void copy_word()
free_all()
```
这些函数不能暴露给别人，应该写成：
```c
static int count_words()
static void copy_word()
static free_all()
```
因为static 表示<font color="red">只能本文件使用</font>，不会污染整个库.

3. **所有文件放在根目录, 如下：**
```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
全部直接放根目录.

4. **不允许提交没有的文件**
例如：
```c
test.c
old.c
abc.c
```
如果Makefile根本不用它们，不要提交.

5. **所有.c文件都必须：**
```bash
-Wall
-Wextra
-Werror
```
能够无Warning编译.

6. **必须使用命令ar**
ar 是 archive 的缩写，是Unix/Linux/macOS 系统中的一个工具，用来把多个目标文件（`.o`）打包成一个 archive 文件.
ar 的主要工作对象是 `.o`

C项目里最典型的用途就是多个.o文件 -> ar -> 一个 .a 静态库.
例如 Libft:
```c
ft_strlen.o
ft_memset.o
ft_memcpy.o
ft_isalpha.o
ft_atoi.o
ft_split.o
...
```
通过:
```bash
</> Bash
ar
```
最终得到:
```bash
libft.a
```
所以:
```bash
.c
 ↓ gcc/cc
.o
 ↓ ar
.a
```
这条链非常重要.

`libft.a` 并不是一个已经运行起来的库，它实际上是一个archive 归档文件, 里面装着很多`.o` 文件，可以粗略理解成：
```c
libft.a
│
├── ft_strlen.o
├── ft_memset.o
├── ft_memcpy.o
├── ft_isalpha.o
├── ft_isdigit.o
├── ft_strdup.o
├── ft_split.o
├── ft_itoa.o
└── ...
```

因此 `ar` 做的事情，本质上就是一个把很多目标文件组织/打包成一个静态库文件.
> 理解命令
> ```bash
>	ar rcs libft.a *.o
> ```
> ar: 调用archive 工具
> rcs:
>	- r = replace 将制定的`.o` 文件加入archive，如果archive中已经存在同名成员，则替换它，不存在则创建它.
>	- c = create 如果archive不存在，则创建archive.
>	- s 为archive创建symbol index 符号索引

命令：
```bash
</> Bash
ar rcs libft.a *.o
```
是最典型的静态库创建方式, 可理解为：
```bash
ar
│
├── r → 把 .o 加进去 / 替换旧版本
├── c → 必要时创建 .a
└── s → 建立符号索引
```

| 工具           | 主要作用           |
| ------------ | -------------- |
| `cc` / `gcc` | 编译 C           |
| `ar`         | 创建/管理 archive  |
| linker       | 把目标文件/库链接成最终程序 |
项目明确要求使用 `ar` 创建 `libft.a`，禁止使用 `libtool`

7. **libft.a 必须位于根目录**
`libft.a` 就在 `Makefile` 旁边.

### 2. README Requirements

`README.md` 是项目的一部分，要求在仓库根目录一定要提供它.

`README` 至少应该包含以下内容：
1. **第1行必须是斜体，并且内容固定为：**
```
*This activity has been created as part of the 42 curriculum by <login>.*
```
如果多人合作，可以依次写多个 login.

2. **Description 项目介绍，说明：**
- Libft 是什么
- 项目目标
- 主要实现内容

3. **Instructions 使用说明**，比如：
- 编译，例如 make
- 生成 `libft.a`
- 在其他项目中使用该静态库

4. **Resources (参考资料)**
列出学习过程中参考的资料，例如：
- C 标准库文档（man pages）
- 教程
- 技术文章等
此外，还必须说明 **AI 在项目中的使用情况**，例如用于概念解释、代码审查或调试，但哪些部分由自己完成.

5. **详细介绍创建的库**
对 `libft`库本身进行详细说明，例如：
- 包含哪些类别的函数
- 每类函数的用途
- 该库在后续 42 项目中的作用